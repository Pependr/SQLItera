import contextlib as cl

from typing import Any, Callable, Iterable, Protocol, Generator

from sqlitera.protocols import Cursor, Aggregate, Connection
from sqlitera.schemes.columns import filter_by_columns


@cl.contextmanager
def cursor(conn: Connection) -> Generator[Cursor, None, None]:
	cur = conn.cursor()
	try:
		yield cur
	finally:
		cur.close()


class CreateScheme(Protocol):
	@property
	def create_query(self) -> str: ...


def create(conn: Connection, scheme: CreateScheme) -> None:
	with cursor(conn) as cur:
		cur.execute(scheme.create_query)


class InsertScheme(Protocol):
	def insert(self, inputs: Iterable[str]) -> str: ...

	@property
	def columns(self) -> Iterable[Any]: ...


def insert(conn: Connection, scheme: InsertScheme, **items: Any) -> None:
	inputs: dict[str, Any] = filter_by_columns(items, scheme.columns)

	with cursor(conn) as cur:
		cur.execute(scheme.insert(inputs), tuple(inputs.values()))


type AggregateFn[I, O] = Callable[[Iterable[Iterable[I]]], O]


def aggregate[I, O](aggr_fn: AggregateFn[I, O]) -> type[Aggregate[I, O]]:
	class AggrCls:
		def __init__(self) -> None:
			self.buffer: list[list[I]] = []

		# @classmethod
		# def __call__(cls, cols: Iterable[Iterable[I]]) -> O:
		# 	return aggr_fn(cols)

		def step(self, *values: I) -> None:
			while len(values) > len(self.buffer):
				self.buffer.append([])

			for val, col in zip(values, self.buffer):
				col.append(val)

		def finalize(self) -> O:
			return aggr_fn(self.buffer)

	return AggrCls
