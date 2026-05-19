import contextlib as cl

from typing import Any, Callable, Iterable, Protocol, Generator

from sqlitera.protocols import Cursor, Aggregate, Connection


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


def insert(conn: Connection, scheme: InsertScheme, **inputs: Any) -> None:
	with cursor(conn) as cur:
		cur.execute(scheme.insert(inputs.keys()), tuple(inputs.values()))


type AggregateFn[I, O] = Callable[[Iterable[Iterable[I]]], O]


def aggregate[I, O](aggr_fn: AggregateFn[I, O]) -> type[Aggregate[I, O]]:
	class AggrCls:
		def __init__(self) -> None:
			self.buffer: list[tuple[I, ...]] = []

		def __call__(self, cols: Iterable[Iterable[I]]) -> O:
			return aggr_fn(cols)

		def step(self, *values: I) -> None:
			self.buffer.append(values)

		def finalize(self) -> O:
			return aggr_fn(self.buffer)

	return AggrCls
