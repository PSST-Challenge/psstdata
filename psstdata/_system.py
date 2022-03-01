import csv
import dataclasses
import inspect
import json
from functools import lru_cache
from typing import Type, TypeVar, Callable, Iterable, Dict

T = TypeVar("T")


def cast_dict(d: Dict[str, any], t: Type[T]) -> T:
    return _cast_dict_factory(t)(d)


@lru_cache()
def _cast_dict_factory(t: Type[T]) -> Callable[[Dict[str, any]], T]:
    # Probably overkill, but trying to future-proof json deserialization a bit.
    spec = inspect.getfullargspec(t.__init__)
    if spec.varkw is not None:
        # **kwargs is present, let 'em have it
        return t
    constructor_args = set(spec.args)

    def cast_discarding_unusable(d: Dict[str, any]) -> T:
        filtered_args = {
            key: value
            for key, value in d.items()
            if key in constructor_args
        }
        return t(**filtered_args)

    return cast_discarding_unusable


def read_json(json_file: str, t: Type[T]) -> T:
    with open(json_file) as f:
        obj = json.load(f)
        return cast_dict(obj, t)


def read_tsv(tsv_file: str, t: Type[T]) -> Iterable[T]:
    items = []
    row_factory = read_tsv_row_factory(t)
    with open(tsv_file) as f:
        reader = csv.reader(f, dialect=csv.excel_tab)
        columns = next(reader)
        for row in reader:
            item = row_factory(columns, row)
            items.append(item)
    return items


@lru_cache()
def read_tsv_row_factory(t: Type[T]) -> Callable[[Iterable[str], Iterable[any]], T]:
    fields = {
        field.name: field.type
        for field in dataclasses.fields(t)
    }

    def cast(columns, row):
        return t(**{
            column: fields[column](value)
            for column, value in zip(columns, row)
        })

    return cast