from __future__ import annotations

from struct import Struct
from typing import Tuple

from .constant import *

le_uint32_sequence_to_16_packer = Struct('<IIIIIIIIIIIIIIII')  # 4 * 16 = 64bytes
le_uint32_sequence_to_8_packer = Struct('<IIIIIIII')  # 4 * 8 = 32bytes


def fnv(a: int, b: int) -> int:
    return ((a * FNV_PRIME) ^ b) & UINT32_MAX_VALUE


def fnv_hash(mix_integers: Tuple[int, ...], data: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(fnv(mix_integers[i], data[i]) for i in range(len(mix_integers)))


def is_prime(number: int) -> bool:
    if number <= 1:
        return False

    for x in range(2, int(number ** 0.5) + 1):
        if number % x == 0:
            return False

    return True


epoch = lambda x: x // EPOCH_SIZE


def cache_size(block_number: int) -> int:
    size = INITIAL_CACHE_SIZE + (CACHE_EPOCH_GROWTH_SIZE * epoch(block_number))
    size -= HASH_BYTES
    while not is_prime(size // HASH_BYTES):
        size -= 2 * HASH_BYTES

    return size


def dataset_size(block_number: int) -> int:
    size = INITIAL_DATASET_SIZE + (DATASET_EPOCH_GROWTH_SIZE * epoch(block_number))
    size -= MIX_BYTES
    while not is_prime(size // MIX_BYTES):
        size -= 2 * MIX_BYTES
    return size
