import pytest as pt
import pytest_mock as pm

import contextlib as cl

import sqlitera.protocols as pts
import sqlitera.operations as ops


@pt.fixture
def cur(mocker: pm.MockerFixture) -> pm.MockType:
	return mocker.Mock(spec_set=pts.Cursor)


@pt.fixture
def conn(mocker: pm.MockerFixture) -> pm.MockType:
	return mocker.Mock(spec_set=pts.Connection)


def test_cursor(conn: pm.MockType, cur: pm.MockType) -> None:
	conn.cursor.return_value = cur

	with ops.cursor(conn):
		...

	conn.cursor.assert_called_once()
	cur.close.assert_called_once()

	conn.reset_mock()
	cur.reset_mock()

	class OopsieDaisy(RuntimeError): ...

	with cl.suppress(OopsieDaisy):
		with ops.cursor(conn):
			raise OopsieDaisy

	conn.cursor.assert_called_once()
	cur.close.assert_called_once()
