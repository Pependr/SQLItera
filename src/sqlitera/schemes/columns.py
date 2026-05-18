from enum import StrEnum
from dataclasses import KW_ONLY, dataclass

from types import EllipsisType
from typing import Any, Callable, Iterable


type ValidatorFn[T] = Callable[[T], bool]


class ValidationError[T](ValueError):
	def __init__(
		self, validator: ValidatorFn[T], value: T, message: str
	) -> None:
		self.validator = validator
		self.value = value
		super().__init__(message)


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

	def validate(self, value: T) -> None:
		for validator in self.validators:
			if not validator(value):
				raise ValidationError(
					validator, value, f"{validator.__name__}({value!r}) = False"
				)


def filter_by_columns(
	items: dict[str, Any], columns: Iterable[Column[Any]]
) -> dict[str, Any]:
	inputs: dict[str, Any] = {}

	for col in columns:
		if col.name not in items:
			if not col.primary_key:
				inputs[col.name] = col.default
			continue

		col.validate(items[col.name])
		inputs[col.name] = items[col.name]

	return inputs
