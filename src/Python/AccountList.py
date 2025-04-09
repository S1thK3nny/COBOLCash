from PyQt6.QtCore import (
    QAbstractTableModel,
    Qt,
    QModelIndex,
)


class AccountsTableModel(QAbstractTableModel):
    def __init__(self, accounts=None):
        super().__init__()
        self._accounts = accounts or []
        self._headers = ["Account #", "Account Holder", "Type", "Balance", "Status"]

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
                # Use the enum's value
                return account.account_type.value
            elif col == 3:
                return f"${account.balance:.2f}"
            elif col == 4:
                return account.status.value
        return None

    def add_account(self, account):
        """Add an account to the model and notify the view."""
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._accounts.append(account)
        self.endInsertRows()

    def remove_account(self, account):
        """Remove an account from the model and notify the view."""
        try:
            row = self._accounts.index(account)
        except ValueError:
            print("Account not found in the model.")
            return
        self.beginRemoveRows(QModelIndex(), row, row)
        self._accounts.pop(row)
        self.endRemoveRows()

    def update_account(self, row, account):
        """Update an account in the model (for example, after editing)."""
        if 0 <= row < len(self._accounts):
            self._accounts[row] = account
            # Notify views that data at this row has changed
            left_index = self.index(row, 0)
            right_index = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(
                left_index, right_index, [Qt.ItemDataRole.DisplayRole]
            )

    def get_account(self, account_number):
        """Get an account by its account number."""
        return self._accounts[account_number]
