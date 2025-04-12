from datetime import datetime


class Transaction:
    def __init__(
        self,
        transaction_id=0,
        transaction_account_number=0,
        transaction_date=None,
        transaction_type="DEPOSIT",
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
            transaction_type (str): The type of the transaction (e.g., DEPOSIT, WITHDRAWAL).
            transaction_amount (float): The amount of the transaction.
            transaction_balance_after (float): The balance after the transaction.
            transaction_description (str): A description of the transaction.
        """
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
        self.transaction_type = data[3]
        self.transaction_amount = float(data[4])
        self.transaction_balance_after = float(data[5])
        self.transaction_description = data[6]
