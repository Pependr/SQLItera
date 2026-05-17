import pytest as pt

from sqlitera.schemes.columns import Types, Column, DefaultError


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


def test_column_default_descriptor() -> None:
	default_col = Column("default", Types.INT, None)
	no_default_col = Column("no_default", Types.INT)

	assert default_col.default is None

	with pt.raises(DefaultError):
		no_default_col.default
