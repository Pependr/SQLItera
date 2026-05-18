from typing import Any, Callable, Iterable, Protocol


class Aggregate[I, O](Protocol):
	def step(self, *values: I) -> None: ...

	def finalize(self) -> O: ...


type Parameters[T] = dict[str, T] | Iterable[T]


class Cursor(Protocol):
	def execute(
		self, sql: str, parameters: Parameters[Any] = (), /
	) -> None: ...

	def executemany(
		self, sql: str, parameters: Iterable[Parameters[Any]]
	) -> None: ...

	def fetchone(self) -> tuple[Any]: ...

	def fetchall(self) -> list[tuple[Any]]: ...

	def close(self) -> None: ...


class Connection(Protocol):
	def cursor(self) -> Cursor: ...

	def create_function(
		self,
		name: str,
		narg: int,
		func: Callable[[Any], Any] | None,
		/,
		*,
		deterministic: bool = False,
	) -> None: ...

	def create_aggregate(
		self,
		name: str,
		n_arg: int,
		aggregate_class: Callable[[], Aggregate[Any, Any]] | None,
		/,
	) -> None: ...
