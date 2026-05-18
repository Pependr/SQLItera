import pytest as pt
import unittest.mock as um

from typing import cast

import sqlitera.operations as ops


@pt.fixture
def cur() -> um.Mock:
	close = um.Mock()
	close.return_value = None

	cur = um.Mock()
	cur.attach_mock(close, "close")

	return cur


@pt.fixture
def conn(cur: um.Mock) -> um.Mock:
	cursor = um.Mock()
	cursor.return_value = cur

	conn = um.Mock()
	conn.attach_mock(cursor, "cursor")

	return conn


@pt.mark.skip
def test_cursor(conn: um.Mock) -> None:
	with ops.cursor(conn) as cur:
		cur = cast(um.Mock, cur)

	cur.assert_called_once()
	conn.assert_called_once()
