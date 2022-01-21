import numpy as np
from libs import dagger, func, constant
from libs.constant import *
import sha3

from libs.func import le_uint32_sequence_to_16_packer, fnv, fnv_hash

dag = dagger.GenDagger(block_number=1)
b'"\xdb")\xccQlF\xd2!\x00\x86\xf1\xabA~\x0b\xd1\xc3\x82|^\xccj\xf7\xd3\xa3?\x8d\xae3+\xabZ\xa3\x1f\xc5\x8eq\xcf\xf2vf\xe8\x1b\xf4\x18w^t\x83\x97C\xca\x9dA\x0f\xdfQM\x00\x9b\xce\xc2'
b'\xe5&1\x84\xc4\x98\\\xa0W\r\x1e\xbd\xf5\x07\x04\x9eB}\xc8l~\x96HW9\xc0\x96\n,\xe4\xe6\xeb8mZ\xa3\x94q\x87b%\xc2<[iD?m]\xb8\x12\x0f\xe3 L\xed\xcf\xef\xd04\x7fi\xec\x1d'
b"P2\xbb\x01\xe2\xf4\x9ey\x1dV\xe1\xfe!k\xeaH\x87\xec\x06\xb1\x85\x9e/\x02_l\xd0)\xd9\x14F \xf0\xd1\xe8\x05\xa9Nf' \xba\xc9}\xa5\x9c\n\x01\x89\xa6K\x0cI/\x18\xca\xb4\xa9\x9e'\xb3z\xb7\xd5"


def fnv(a: int, b: int) -> int:
    print(a, b)
    return ((a * FNV_PRIME) ^ b) & UINT32_MAX_VALUE


arr = np.array([0, 1, 2])

start_byte = (arr % dag.cache_length) * HASH_BYTES
end_byte = start_byte + HASH_BYTES
for index, s, e in zip(arr, start_byte, end_byte):
    dd = int.from_bytes(dag.cache_bytes[s:e], 'little')
    ee = dd ^ index
    ff = ee.to_bytes(HASH_BYTES, 'little')
    mix = sha3.keccak_512(ff).digest()
    mix_integers = le_uint32_sequence_to_16_packer.unpack(mix)

    for j in range(256):
        mix_word = mix_integers[j % 16]
        cache_index = fnv(index ^ j, mix_word) % dag.cache_length
        parent = dag.cache[cache_index]
        mix_integers = fnv_hash(mix_integers, parent)
    mix = le_uint32_sequence_to_16_packer.pack(*mix_integers)
    print(sha3.keccak_512(mix).digest())

# start_byte = (index % self.cache_length) * HASH_BYTES

# dataset_size = func.dataset_size(1)
# dataset_length = dataset_size // constant.HASH_BYTES
# for idx in dataset_size // constant.HASH_BYTES:
#
#
# print(dag.generate_dataset_item(1))
