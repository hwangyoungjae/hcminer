from __future__ import annotations

import struct
from functools import cached_property
from typing import Tuple

import pyethash
import sha3

from .abstract import AbstractDagger
from ..constant import *
from ..func import le_uint32_sequence_to_16_packer, dataset_size, fnv, fnv_hash, cache_size


class GenDagger(AbstractDagger):
    def __init__(self, block_number: int):
        self.block_number = block_number

    @cached_property
    def cache_size(self) -> int:  # cache size(bytes)
        return cache_size(self.block_number)

    @cached_property
    def dataset_size(self) -> int:
        return dataset_size(self.block_number)

    @cached_property
    def cache_bytes(self) -> bytes:
        return pyethash.mkcache_bytes(self.block_number)  # output little endian

    @cached_property
    def cache(self) -> Tuple[Tuple[int]]:
        fmt = '>' + ('64s' * (len(self.cache_bytes) // 64))
        return tuple(le_uint32_sequence_to_16_packer.unpack(x) for x in struct.unpack(fmt, self.cache_bytes))

    @cached_property
    def cache_length(self) -> int:  # cache array size(count)
        return self.cache_size // HASH_BYTES

    def generate_dataset_item(self, index) -> bytes:
        start_byte = (index % self.cache_length) * HASH_BYTES
        end_byte = start_byte + HASH_BYTES
        dd = int.from_bytes(self.cache_bytes[start_byte:end_byte], 'little')
        ee = dd ^ index
        ff = ee.to_bytes(HASH_BYTES, 'little')
        mix = sha3.keccak_512(ff).digest()

        mix_integers = le_uint32_sequence_to_16_packer.unpack(mix)

        for j in range(DATASET_PARENTS):
            mix_word = mix_integers[j % 16]
            cache_index = fnv(index ^ j, mix_word) % self.cache_length
            parent = self.cache[cache_index]
            mix_integers = fnv_hash(mix_integers, parent)

        mix = le_uint32_sequence_to_16_packer.pack(*mix_integers)
        return sha3.keccak_512(mix).digest()

    def fetch_dataset_item(self, index: int) -> Tuple[int, ...]:
        return le_uint32_sequence_to_16_packer.unpack(self.generate_dataset_item(index))
