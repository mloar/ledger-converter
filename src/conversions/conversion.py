from abc import ABC, abstractmethod
from csv import DictReader

from src.transaction import Transaction


class Conversion(ABC):

    @abstractmethod
    def canConvert(self, heading: str) -> bool:
        """
        Returns TRUE if conversion class can convert file.
        """
        raise NotImplementedError

    @abstractmethod
    def convert(
        self,
        heading: str,
        csv_reading: DictReader,
    ) -> list[Transaction]:
        """
        Conversion of file into transaction list.

        Returns:
        list[Transaction]: All transactions in file
        """
        raise NotImplementedError
