from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)


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

    def add_account(self, account):
        self._all_accounts.append(account)
        self.update_filters()

    def remove_account(self, account):
        try:
            self._all_accounts.remove(account)
        except ValueError:
            print("Account not found in full list.")
            return
        self.update_filters()

    def update_account(self, row, account):
        # Update based on visible row in filtered list
        if 0 <= row < len(self._accounts):
            real_index = self._all_accounts.index(self._accounts[row])
            self._all_accounts[real_index] = account
        self.update_filters()

    def get_account(self, visible_row):
        if 0 <= visible_row < len(self._accounts):
            return self._accounts[visible_row]
        return None

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
