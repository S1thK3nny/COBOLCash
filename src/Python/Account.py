from datetime import datetime
from enum import Enum


# Define Enums for account status and type
class AccountStatus(Enum):
    ACTIVE = "Active"
    FROZEN = "Frozen"
    CLOSED = "Closed"


class AccountType(Enum):
    CHECKING = "Checking"
    SAVINGS = "Savings"
    CREDIT = "Credit"
    LOAN = "Loan"


class Account:
    def __init__(
        self,
        account_number=0,
        account_holder="John Doe",
        account_type=AccountType.CHECKING,
        balance=0.0,
        status=AccountStatus.ACTIVE,
        creation_date=None,
    ):
        """
        Initializes an account with the given parameters.

        Args:
            account_number (int): The account number.
            account_holder (str): The name of the account holder.
            account_type (AccountType): The type of the account (e.g., Checking, Savings).
            balance (float): The initial balance of the account.
            status (AccountStatus): The status of the account (e.g., Active, Frozen, Closed).
            creation_date (datetime): The date the account was created.
        """
        # Ensure that account_type and status are enum instances
        if not isinstance(account_type, AccountType):
            account_type = AccountType(account_type)
        if not isinstance(status, AccountStatus):
            status = AccountStatus(status)

        self.account_number = account_number
        self.account_holder = account_holder
        self.account_type = account_type
        self.balance = balance
        self.status = status
        self.creation_date = creation_date if creation_date else datetime.now()

    def to_dict(self):
        """
        Converts the account object to a dictionary.

        Returns:
            dict: A dictionary representation of the account.
        """
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "account_type": self.account_type.value,
            "balance": self.balance,
            "status": self.status.value,
            "creation_date": (
                self.creation_date.strftime("%Y-%m-%d") if self.creation_date else None
            ),
        }

    def __str__(self):
        return (
            f"Account #{self.account_number}: {self.account_holder} "
            f"({self.account_type.value}) - ${self.balance:.2f} - {self.status.value} - "
            f"{self.creation_date.strftime('%Y-%m-%d')}"
        )


# Example integration with a GUI layout (e.g., using PyQt)
# Here's a simplified snippet for setting up QComboBox with the enums:

# Assume you have the following imports and a QWidget layout already established:
#
# from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QComboBox, QWidget, QApplication
#
# class AccountSearchWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         # Layout setup
#         self.search_layout = QHBoxLayout(self)
#         self.search_input = QLineEdit()
#         self.search_input.setPlaceholderText("Search by account number or name...")
#         self.search_button = QPushButton("Search")
#
#         # Using enum values for status combo box
#         self.filter_status = QComboBox()
#         # Adding a default option
#         self.filter_status.addItem("All Accounts", None)
#         for status in AccountStatus:
#             self.filter_status.addItem(status.value, status)
#
#         # Using enum values for account type combo box
#         self.filter_type = QComboBox()
#         self.filter_type.addItem("All Types", None)
#         for acc_type in AccountType:
#             self.filter_type.addItem(acc_type.value, acc_type)
#
#         # Adding widgets to the layout
#         self.search_layout.addWidget(self.search_input)
#         self.search_layout.addWidget(self.search_button)
#         self.search_layout.addWidget(self.filter_status)
#         self.search_layout.addWidget(self.filter_type)
#
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     window = AccountSearchWidget()
#     window.show()
#     sys.exit(app.exec_())
