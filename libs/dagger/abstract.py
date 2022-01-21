from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Tuple


class AbstractDagger(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, block_number: int): ...

    @abstractmethod
    def fetch_dataset_item(self, index: int) -> Tuple[int, ...]: ...
