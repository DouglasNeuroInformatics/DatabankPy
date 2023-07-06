import json

from typing import Any, Callable, Iterable, TypeVar

import numpy as np

T = TypeVar('T')

def find(iterable: Iterable[T], callback: Callable[[T], bool]) -> T | None:
    for element in iterable:
        if callback(element):
            return element
    return None

def find_index(iterable: list[T], callback: Callable[[T], bool]) -> int | None:
    for i in range(len(iterable)):
        if callback(iterable[i]):
            return i
    return None

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj: object) -> Any:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
