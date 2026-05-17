from dataclasses import dataclass

from typing import Protocol, Collection


class Column(Protocol):
	@property
	def create_query(self) -> str: ...


@dataclass(slots=True, init=False)
class Table:
	name: str
	columns: tuple[Column, ...]

	def __init__(self, name: str, *cols: Column) -> None:
		self.name = name
		self.columns = cols

	@property
	def create_query(self) -> str:
		return f"CREATE TABLE {self.name} ({", ".join(col.create_query for col in self.columns)})"

	def insert_query(self, inputs: Collection[str]) -> str:
		return f"INSERT INTO {self.name} ({", ".join(inputs)}) VALUES ({", ".join("?" * len(inputs))})"
