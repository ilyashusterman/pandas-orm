from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class DescribeDataFrameTable:
    name: str
    columns: DataFrame
    indexes: DataFrame

    def __str__(self):
        return f'Table {self.name}\n{self.columns.to_string()}' \
               f'\nIndexes\n{self.indexes.to_string()}'

    def __repr__(self):
        return self.__str__()