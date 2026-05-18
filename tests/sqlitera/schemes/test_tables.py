import pytest as pt
import unittest.mock as um

from typing import Any

from sqlitera.schemes.tables import Table


@pt.fixture
def mock() -> um.Mock:
	return um.Mock()


@pt.fixture
def mock_col(mock: um.Mock) -> um.Mock:
	mock.create_query = "MOCKER COLUMN"
	return mock


@pt.fixture
def test_table(mock_col: um.Mock) -> Table:
	return Table(
		"test",
		mock_col,
		mock_col,
		mock_col,
	)


def test_table_create_query(test_table: Table) -> None:
	assert (
		test_table.create_query
		== "CREATE TABLE test (MOCKER COLUMN, MOCKER COLUMN, MOCKER COLUMN)"
	)


def test_table_insert_query(test_table: Table) -> None:
	data: dict[str, Any] = {
		"test1": 69,
		"test2": 6.7,
		"test3": "bruh",
	}

	assert (
		test_table.insert_query(data)
		== "INSERT INTO test (test1, test2, test3) VALUES (:test1, :test2, :test3)"
	)
