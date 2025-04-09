from datetime import datetime


class Account:
    def __init__(
        self,
        account_number=0,
        account_holder="John Doe",
        account_type="Checking",
        balance=0.0,
        status="Active",
        creation_date=None,
    ):
        """
        Initializes an account with the given parameters.

        Args:
            account_number (int): The account number.
            account_holder (str): The name of the account holder.
            account_type (str): The type of the account (e.g., Checking, Savings).
            balance (float): The initial balance of the account.
            status (str): The status of the account (e.g., Active, Inactive).
            creation_date (date): The date the account was created.
        """
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
            "account_type": self.account_type,
            "balance": self.balance,
            "status": self.status,
            "creation_date": (
                self.creation_date.strftime("%Y-%m-%d") if self.creation_date else None
            ),
        }

    def __str__(self):
        return f"Account #{self.account_number}: {self.account_holder} ({self.account_type}) - ${self.balance:.2f} - {self.status} - {self.creation_date})"
