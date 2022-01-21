import time

from libs.ethash import Ethash
from libs import dagger
import binascii

if __name__ == '__main__':
    recv_pow_hash = '0x0fa92a2afdba20b3e75911666bd9d8b5713c11913d2b002f999b2e9e21dae398'
    recv_target = '0x00000000ffff00000000ffff00000000ffff00000000ffff00000000ffff0000'
    recv_block_number = '0xd60ce5'

    ethash = Ethash(
        pow_hash=binascii.unhexlify(recv_pow_hash[2:]),
        target=binascii.unhexlify(recv_target[2:]),
        block_number=eval(recv_block_number),
        dagger_cls=dagger.GethDagger,
    )

    nonce = 0xea66061fc505700e
    s = time.time()
    r = ethash.hashimoto(nonce)
    print(time.time() - s)
    print(r['mix_digest'].hex() == '8a2b9369ebfdb7754910761d244377cc9cc307436d022e36da634f49af07d098')
    print(r['mix_digest'].hex())
    print(r['result'].hex())
