"""
Transaction.py

This module defines the Transaction class and its associated methods.
It includes the TransactionType enum for different transaction types.
"""

from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    """
    Enum representing different types of transactions.
    - DEPOSIT: Money added to the account.
    - WITHDRAWAL: Money taken from the account.
    - TRANSFER: Money moved between accounts.
    - INTEREST: Interest added to the account.
    - FEE: Fees deducted from the account.
    """

    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"
    INTEREST = "INTEREST"
    FEE = "FEE"


class Transaction:
    def __init__(
        self,
        transaction_id=0,
        transaction_account_number=0,
        transaction_date=None,
        transaction_type=TransactionType.DEPOSIT,
        transaction_amount=0,
        transaction_balance_after=0,
        transaction_description="",
    ):
        """
        Initializes a transaction with the given parameters.

        Args:
            transaction_id (int): The transaction ID.
            transaction_account_number (int): The account number associated with the transaction.
            transaction_date (datetime): The date of the transaction.
            transaction_type (TransactionType): The type of the transaction (e.g., Deposit).
            transaction_amount (float): The amount of the transaction.
            transaction_balance_after (float): The balance after the transaction.
            transaction_description (str): A description of the transaction.
        """
        if not isinstance(transaction_type, TransactionType):
            transaction_type = TransactionType(transaction_type)

        self.transaction_id = transaction_id
        self.transaction_account_number = transaction_account_number
        self.transaction_date = transaction_date if transaction_date else datetime.now()
        self.transaction_type = transaction_type
        self.transaction_amount = transaction_amount
        self.transaction_balance_after = transaction_balance_after
        self.transaction_description = transaction_description
        self.transaction_date_str = (
            self.transaction_date.strftime("%Y-%m-%d")
            if self.transaction_date
            else None
        )

    def from_list(self, data):
        """
        Populates the transaction object from a list.
        Args:
            data (list): A list containing transaction data.
        """
        self.transaction_id = int(data[0])
        self.transaction_account_number = int(data[1])
        self.transaction_date = datetime.strptime(data[2], "%Y-%m-%d")
        self.transaction_type = TransactionType(data[3].upper())
        self.transaction_amount = float(data[4])
        self.transaction_balance_after = float(data[5])
        self.transaction_description = data[6]
