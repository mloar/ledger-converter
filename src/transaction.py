import datetime


class Transaction:

    def __init__(
        self,
        date: str,
        description: str,
        value: float,
        payee: str,
        account: str,
    ):

        format = "%m/%d/%Y"
        try:
            datetime_str = datetime.datetime.strptime(date, format)
        except ValueError:
            format = "%Y-%m-%d"
            datetime_str = datetime.datetime.strptime(date, format)

        self.date = datetime_str
        self.description = description
        self.value = value
        self.payee = payee
        self.account = account

    def exportString(self) -> str:
        """
        Exports transaction to a Ledger format

        Returns:
        str: transaction in Ledger format
        """
        return (
            f'{self.date.strftime("%Y-%m-%d")}       {self.description}\n'
            f"    {self.payee}                            ${self.value}\n"
            f"    {self.account}\n\n"
        )

    def toString(self) -> str:
        return (
            f"{self.date} - "
            f"{self.description} - "
            f"{self.value} - "
            f"{self.payee} - "
            f"{self.account}"
        )
