from dataclasses import dataclass

from typing import Iterable, Protocol


class Createable(Protocol):
	@property
	def create_query(self) -> str: ...


@dataclass(slots=True, init=False)
class Table:
	name: str
	columns: tuple[Createable, ...]

	def __init__(self, name: str, *cols: Createable) -> None:
		self.name = name
		self.columns = cols

	@property
	def create_query(self) -> str:
		return f"CREATE TABLE {self.name} ({", ".join(col.create_query for col in self.columns)})"

	def insert_query(self, inputs: Iterable[str]) -> str:
		return f"INSERT INTO {self.name} ({", ".join(inputs)}) VALUES ({", ".join(f":{i}" for i in inputs)})"
