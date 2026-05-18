import pytest as pt

from typing import Any

from sqlitera.schemes.columns import (
	Types,
	Column,
	ValidatorFn,
	DefaultError,
	ValidationError,
	filter_by_columns,
)


@pt.fixture
def validators() -> tuple[ValidatorFn[str], ValidatorFn[str]]:
	def len_over_3(s: str) -> bool:
		return len(s) > 3

	def valid_var(s: str) -> bool:
		return s[0] not in " 0123456789"

	return (len_over_3, valid_var)


def test_column_query() -> None:
	col1 = Column("test1", Types.NONE)
	col2 = Column("test2", Types.INT, unique=True)
	col3 = Column("test3", Types.BYTES, primary_key=True)
	col4 = Column("test4", Types.FLOAT, not_null=True)
	col5 = Column(
		"test5", Types.STR, unique=True, primary_key=True, not_null=True
	)

	assert col1.create_query == "test1 NULL"
	assert col2.create_query == "test2 INTEGER UNIQUE"
	assert col3.create_query == "test3 BLOB PRIMARY KEY"
	assert col4.create_query == "test4 REAL NOT NULL"
	assert col5.create_query == "test5 TEXT NOT NULL UNIQUE PRIMARY KEY"


def test_column_default_property() -> None:
	default_col = Column("default", Types.INT, None)
	no_default_col = Column("no_default", Types.INT)

	assert default_col.default is None

	with pt.raises(DefaultError):
		no_default_col.default


def test_column_validate(
	validators: tuple[ValidatorFn[str], ValidatorFn[str]],
) -> None:
	col = Column("valid", Types.STR, validators=validators)

	col.validate("Alice")

	with pt.raises(ValidationError):
		col.validate("1a")


def test_filter_by_columns(
	validators: tuple[ValidatorFn[str], ValidatorFn[str]],
) -> None:
	cols = (
		Column("prim_key", Types.INT, primary_key=True),
		Column("defaulted", Types.STR, "Bob"),
		Column("validated", Types.STR, validators=validators),
	)

	sample1: tuple[dict[str, Any], dict[str, Any]] = (
		{"prim_key": 0, "defaulted": "Alice", "validated": "Smith"},
		{"prim_key": 0, "defaulted": "Alice", "validated": "Smith"},
	)

	sample2: tuple[dict[str, Any], dict[str, Any]] = (
		{"defaulted": "Alice", "validated": "Smith"},
		{"defaulted": "Alice", "validated": "Smith"},
	)

	sample3: dict[str, Any] = {"prim_key": 0, "defaulted": "Alice"}

	sample4: dict[str, Any] = {
		"prim_key": 0,
		"defaulted": "Alice",
		"validated": "123",
	}

	assert filter_by_columns(sample1[0], cols) == sample1[1]
	assert filter_by_columns(sample2[0], cols) == sample2[1]

	with pt.raises(DefaultError):
		filter_by_columns(sample3, cols)

	with pt.raises(ValidationError):
		filter_by_columns(sample4, cols)
