from __future__ import annotations

from typing import Type, Tuple

import sha3

from . import dagger
from . import func
from .constant import MIX_BYTES, HASH_BYTES, HASHIMOTO_ACCESSES
from .func import le_uint32_sequence_to_16_packer, fnv, fnv_hash, le_uint32_sequence_to_8_packer


class Ethash(object):
    def __init__(self,
                 pow_hash: bytes,  # 32bytes
                 target: bytes,  # 32bytes
                 block_number: int,
                 dagger_cls: Type[dagger.AbstractDagger] = None,
                 ):
        self.pow_hash = pow_hash
        self.target = target
        self.block_number = block_number
        self.dataset_size = func.dataset_size(self.block_number)
        self.dagger = dagger.GenDagger(self.block_number) if dagger_cls is None else dagger_cls(self.block_number)
        print('block_number :', self.block_number)
        print('pow_hash     :', self.pow_hash.hex())
        print('target       :', self.target.hex())

    def hashimoto(self,
                  nonce: int  # 8bytes
                  ):
        nonce_le = nonce.to_bytes(8, 'little')
        seed_hash = sha3.keccak_512(self.pow_hash + nonce_le).digest()
        seed_head = int.from_bytes(seed_hash[:4], "little")

        mix = le_uint32_sequence_to_16_packer.unpack(seed_hash) * (MIX_BYTES // HASH_BYTES)
        mix_length = len(mix)

        rows = self.dataset_size // 128
        for i in range(HASHIMOTO_ACCESSES):
            new_data: Tuple[int, ...] = ()
            ii = i ^ seed_head
            iii = i % mix_length
            parent = fnv(ii, mix[iii]) % rows
            for j in range(MIX_BYTES // HASH_BYTES):
                index = 2 * parent + j
                new_data += self.dagger.fetch_dataset_item(index)
            mix = fnv_hash(mix, new_data)

        # 후처리 함수
        compressed_mix = []
        for i in range(0, len(mix), 4):
            aa = fnv(mix[i], mix[i + 1])
            bb = fnv(aa, mix[i + 2])
            cc = fnv(bb, mix[i + 3])
            compressed_mix.append(cc)

        mix_digest = le_uint32_sequence_to_8_packer.pack(*compressed_mix)
        result = sha3.keccak_256(seed_hash + mix_digest).digest()
        return {
            'mix_digest': mix_digest,
            'result': result,
        }
