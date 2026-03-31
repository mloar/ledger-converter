import re

from csv import DictReader

from src.accounts import Accounts
from src.conversions.conversion import Conversion
from src.transaction import Transaction


class WintrustConversion(Conversion):

    HEADER = ["Date","Account","Description","Check #","Category","Memo","Credit","Debit"]

    def __init__(self, accounts: Accounts):
        self.account = accounts

    def canConvert(self, heading: str) -> bool:
        return len(heading) == 2 and re.match(r'\*+\d\d\d\d', heading[1])

    def convert(
        self,
        heading: str,
        csv_reader: DictReader,
    ) -> list[Transaction]:

        print(heading)
        # Move reader cursor until the beginning of data
        row = heading
        while row != WintrustConversion.HEADER:
            row = next(csv_reader)

        transactions = []

        for row in csv_reader:
            date = row[0]
            if not date:
                break
            description = row[2]
            value = float(row[6] or row[7])

            # Transaction to buy something from someone
            if value < 0:
                value = value * -1

                account = self.account.getAccount(
                    Accounts.DEFAULT_BANK,
                    "Checking",
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
                    "Checking",
                )

            if description.startswith("Beginning balance"):
                continue

            transaction = Transaction(date, description, value, payee, account)
            transactions.append(transaction)

        return transactions
