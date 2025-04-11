# pylint: disable=no-name-in-module
# pylint: disable=import-error

from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)
from Account import Account, AccountStatus
from COBOLInterface import COBOL_call, COBOL_get_account


class AccountsTableModel(QAbstractTableModel):
    def __init__(self, accounts=None):
        super().__init__()
        self._all_accounts = accounts or []
        self._accounts = list(self._all_accounts)  # filtered view
        self._headers = ["Account #", "Account Holder", "Type", "Balance", "Status"]

        # Filters
        self._filter_text = ""
        self._filter_status = None
        self._filter_type = None

    def rowCount(self, parent=QModelIndex()):
        return len(self._accounts)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._accounts)):
            return None

        account = self._accounts[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            col = index.column()
            if col == 0:
                return account.account_number
            elif col == 1:
                return account.account_holder
            elif col == 2:
                return account.account_type.value
            elif col == 3:
                return f"${account.balance:.2f}"
            elif col == 4:
                return account.status.value
        return None

    def add_account(self, account_holder, account_type, balance) -> Account:
        response = COBOL_call(
            f"CREATE-ACCOUNT|{account_holder}|{account_type.value}|{balance}"
        )
        if response.startswith("ERROR"):
            print("Error creating account:", response)
            return
        account = COBOL_get_account(response.split("|")[1])
        if not account:
            print("Error fetching created account.")
            return
        self._all_accounts.append(account)
        self.update_filters()
        print("Account created successfully:", account)
        return account

    def close_account(self, account: Account):
        # Keep the account, but close it
        try:
            response = COBOL_call(
                f"UPDATE-ACCOUNT|{account.account_number}|STATUS|Closed"
            )
            if response.startswith("ERROR"):
                print("Error deleting account:", response)
                return
        except ValueError:
            print("Account not found in full list.")
            return
        account.status = AccountStatus.CLOSED
        self.update_filters()
        print("Account closed successfully:", account)

    def update_account(self, account: Account, updated_fields: dict):
        """
        Update specific fields of an account in the filtered view and propagate to the backend.

        Args:
            row: The visible row index in the filtered view.
            updated_fields: Dict of fields to update, e.g. {"balance": 2000.0}
        """
        if not account in self._all_accounts:
            print("Invalid account")
            return

        # Apply changes locally
        changed_fields = []
        for field, new_value in updated_fields.items():
            if hasattr(account, field):
                old_value = getattr(account, field)
                if old_value != new_value:
                    setattr(account, field, new_value)
                    changed_fields.append(field)
            else:
                print(f"Warning: Unknown field '{field}' ignored.")

        if not changed_fields:
            print("No changes detected.")
            return

        for field in changed_fields:
            value = getattr(account, field)
            if hasattr(value, "value"):  # Enum to string
                value = value.value
            command = f"UPDATE-ACCOUNT|{account.account_number}|{field.upper()}|{value}"
            response = COBOL_call(command)
            if response.startswith("ERROR"):
                print(
                    f"Error updating field '{field}' for account {account.account_number}: {response}"
                )
                return

        # Update succeeded, trigger UI refresh
        self.update_filters()

        print(f"Account {account.account_number} updated: {changed_fields}")

    def remove_account(self, account: Account) -> bool:
        try:
            response = COBOL_call(f"DELETE-ACCOUNT|{account.account_number}")
            if response.startswith("ERROR"):
                print("Error deleting account:", response)
                return False
        except ValueError:
            print("Account not found in full list.")
            return False
        self._all_accounts.remove(account)
        self.update_filters()
        print("Account removed successfully:", account)
        return True

    # TODO: Update the method to not use the visible row but straight up get it from COBOL backend
    def get_account(self, visible_row: int):
        if 0 <= visible_row < len(self._accounts):
            return self._accounts[visible_row]
        return None

    def process_transaction(
        self, type: str, account_number: int, amount: float, description: str
    ):
        """
        Process a transaction for a given account.

        Args:
            account: The account to process the transaction on.
            amount: The amount to deposit or withdraw (negative for withdrawal).
        """
        account = self.get_account_by_id(account_number)
        if not account:
            print("Account not found.")
            return

        command = f"TRANSACTION|{type}|{account_number}|{amount}|{description}"
        response = COBOL_call(command)
        if response.startswith("ERROR"):
            print("Error processing transaction:", response)
            return

        # Update succeeded, trigger UI refresh
        account.balance = float(response.split("|")[3])
        amount_str = response.split("|")[4].replace("\nOK", "")  # Remove the \nOK
        amount = float(amount_str)
        self.update_filters()
        print(
            f"Transaction processed successfully: {type} {amount} for account {account.account_number}"
        )

    def set_filters(self, text="", status=None, acc_type=None):
        self.beginResetModel()
        self._filter_text = text.lower().strip()
        self._filter_status = status
        self._filter_type = acc_type

        self._accounts = [
            acc
            for acc in self._all_accounts
            if (
                not self._filter_text
                or self._filter_text in acc.account_holder.lower()
                or self._filter_text in str(acc.account_number)
            )
            and (status is None or acc.status == status)
            and (acc_type is None or acc.account_type == acc_type)
        ]
        self.endResetModel()

    def update_filters(self):
        self.set_filters(self._filter_text, self._filter_status, self._filter_type)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()

        def sort_key(account):
            return {
                0: account.account_number,
                1: account.account_holder.lower(),
                2: account.account_type.value,
                3: account.balance,
                4: account.status.value,
            }[column]

        reverse = order == Qt.SortOrder.DescendingOrder
        self._accounts.sort(key=sort_key, reverse=reverse)

        self.layoutChanged.emit()

    def get_account_by_id(self, account_number):
        """
        Find and return an account by its account number.
        Searches first in the local cache, then falls back to COBOL backend if not found.

        Args:
            account_number: The account number to search for

        Returns:
            Account object if found, None otherwise
        """
        # First try to find in our cached accounts
        for account in self._all_accounts:
            if account.account_number == account_number:
                return account

        # If not found locally, try to fetch from COBOL backend
        return COBOL_get_account(account_number)
