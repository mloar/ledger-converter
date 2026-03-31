from csv import DictReader

from src.accounts import Accounts
from src.conversions.conversion import Conversion
from src.transaction import Transaction


class ChaseConversion(Conversion):

    HEADER = ["Transaction Date","Post Date","Description","Category","Type","Amount","Memo"]

    def __init__(self, accounts: Accounts):
        self.account = accounts

    def canConvert(self, heading: str) -> bool:
        return heading == ChaseConversion.HEADER

    def convert(
        self,
        heading: str,
        csv_reader: DictReader,
    ) -> list[Transaction]:

        # Move reader cursor until the beginning of data
        row = heading
        while row != ChaseConversion.HEADER:
            row = next(csv_reader)
        row = next(csv_reader)

        transactions = []

        for row in csv_reader:
            date = row[0]
            if not date:
                break
            description = row[2]
            value = float(row[5])

            # Transaction to buy something from someone
            if value < 0:
                value = value * -1

                account = self.account.getAccount(
                    Accounts.DEFAULT_BANK,
                    "CreditCard",
                )
                payee = self.account.getAccount(
                    Accounts.DEFAULT_EXPENSES,
                    description,
                )

            # Transaction to pay one of my accounts
            else:
                self.value = value
                account = self.account.getAccount(
                    Accounts.DEFAULT_LIABILITY,
                    description,
                )
                payee = self.account.getAccount(
                    Accounts.DEFAULT_BANK,
                    "CreditCard",
                )

            if description.startswith("Beginning balance"):
                continue

            transaction = Transaction(date, description, value, payee, account)
            transactions.append(transaction)

        return transactions
