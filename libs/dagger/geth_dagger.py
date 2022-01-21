from __future__ import annotations

import os
from typing import Tuple

from .abstract import AbstractDagger
from ..constant import *
from ..func import le_uint32_sequence_to_16_packer


class GethDagger(AbstractDagger):
    MAGIC_NUMBER_LENGTH = 8

    def __init__(self, block_number: int):
        self.epoch = block_number // EPOCH_SIZE
        path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'include', 'dataset', str(self.epoch)))
        self._f = open(path, 'rb')

    def fetch_dataset_item(self, index: int) -> Tuple[int, ...]:
        self._f.seek(self.MAGIC_NUMBER_LENGTH + (HASH_BYTES * index))
        return le_uint32_sequence_to_16_packer.unpack(self._f.read(HASH_BYTES))

    def __del__(self):
        try:
            self._f.close()
        except Exception:
            pass
