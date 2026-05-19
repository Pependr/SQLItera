import pytest as pt
import pytest_mock as pm

import contextlib as cl

from typing import Iterable, cast

import sqlitera.protocols as pts
import sqlitera.operations as ops


@pt.fixture
def cur(mocker: pm.MockerFixture) -> pm.MockType:
	return mocker.Mock(spec_set=pts.Cursor)


@pt.fixture
def conn(mocker: pm.MockerFixture) -> pm.MockType:
	return mocker.Mock(spec_set=pts.Connection)


def test_cursor(
	conn: pm.MockType, cur: pm.MockType, subtests: pt.Subtests
) -> None:
	conn.cursor.return_value = cur

	with subtests.test("Error on cursor() call"):
		with ops.cursor(conn):
			...

		conn.cursor.assert_called_once()
		cur.close.assert_called_once()

	conn.reset_mock()
	cur.reset_mock()

	class OopsieDaisy(RuntimeError): ...

	with subtests.test("Error on cursor() call with exception"):
		with cl.suppress(OopsieDaisy):
			with ops.cursor(conn):
				raise OopsieDaisy

		conn.cursor.assert_called_once()
		cur.close.assert_called_once()


def test_create(
	mocker: pm.MockerFixture, conn: pm.MockType, cur: pm.MockType
) -> None:
	conn.cursor.return_value = cur

	mock_scheme = mocker.Mock(spec_set=ops.CreateScheme)
	mock_scheme.create_query = "CREATE MOCK"

	ops.create(conn, mock_scheme)

	cur.execute.assert_called_once_with("CREATE MOCK")


def test_insert(
	mocker: pm.MockerFixture, conn: pm.MockType, cur: pm.MockType
) -> None:
	conn.cursor.return_value = cur

	mock_scheme = mocker.Mock(spec_set=ops.InsertScheme)
	mock_scheme.insert.return_value = "INSERT INTO MOCK"

	data: dict[str, int] = {f"mock{i}": i for i in range(1, 4)}

	ops.insert(conn, mock_scheme, **data)

	mock_scheme.insert.assert_called_once_with(data.keys())
	cur.execute.assert_called_once_with("INSERT INTO MOCK", (1, 2, 3))


def test_aggregate(mocker: pm.MockerFixture, subtests: pt.Subtests) -> None:
	def my_aggregate(cols: Iterable[Iterable[int]]) -> int:
		return sum(sum(row) for row in cols)

	mock_aggr_fn = mocker.Mock(wraps=my_aggregate)

	aggr_obj = cast(pts.Aggregate[int, int], ops.aggregate(mock_aggr_fn)())

	sample: list[list[int]] = [
		[1, 2, 3],
		[4, 5, 6],
		[7, 8, 9],
	]

	with subtests.test("Error on calling aggregate object"):
		assert aggr_obj(sample) == my_aggregate(sample)
		mock_aggr_fn.assert_called_once_with(sample)

	mock_aggr_fn.reset_mock()

	with subtests.test("Error on using aggregate object"):
		for row in sample:
			aggr_obj.step(*row)

		assert aggr_obj.finalize() == my_aggregate(sample)

		mock_aggr_fn.assert_called_once_with([(1, 2, 3), (4, 5, 6), (7, 8, 9)])
