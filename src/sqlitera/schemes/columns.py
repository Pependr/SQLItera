from enum import StrEnum
from dataclasses import KW_ONLY, dataclass

from types import EllipsisType
from typing import Callable


type ValidatorFn[T] = Callable[[T], bool]


class DefaultError(ValueError): ...


class Types(StrEnum):
	INT = "INTEGER"
	STR = "TEXT"
	FLOAT = "REAL"
	NONE = "NULL"
	BYTES = "BLOB"


@dataclass(frozen=True, slots=True)
class Column[T]:
	name: str
	type: Types
	__default__: T | EllipsisType = ...
	_: KW_ONLY
	not_null: bool = False
	unique: bool = False
	primary_key: bool = False
	validators: tuple[ValidatorFn[T], ...] = ()

	@property
	def default(self) -> T:
		if self.__default__ is ...:
			raise DefaultError("No default value provided")
		return self.__default__

	@property
	def create_query(self) -> str:
		query: list[str] = [self.name, self.type]

		if self.not_null:
			query.append("NOT NULL")

		if self.unique:
			query.append("UNIQUE")

		if self.primary_key:
			query.append("PRIMARY KEY")

		return " ".join(query)
