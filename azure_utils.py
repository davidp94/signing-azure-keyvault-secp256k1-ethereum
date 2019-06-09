import secp256k1

CURVE_ORDER = 115792089237316195423570985008687907852837564279074904382605163141518161494337
HALF_CURV_ORDER = 57896044618658097711785492504343953926418782139537452191302581570759080747168


def is_high(s):
    return s > HALF_CURV_ORDER


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def make_canonical(sig_bytes):
    r = sig_bytes[0:32]
    s = sig_bytes[32:64]

    r_int = int_from_bytes(r)
    s_int = int_from_bytes(s)

    if is_high(s_int):
        s_int = CURVE_ORDER - s_int

    canonical = bytearray()
    r = int_to_bytes(r_int)
    s = int_to_bytes(s_int)
    canonical.extend(r)
    canonical.extend(s)
    return canonical


class MyECDSA(secp256k1.Base, secp256k1.ECDSA):
    def __init__(self):
        secp256k1.Base.__init__(self, ctx=None, flags=secp256k1.ALL_FLAGS)


def convert_azure_secp256k1_signature_to_vrs(pub_key_bytes, msg_hash_bytes, sig_bytes, chain_id=0):
    sig_bytes = bytes(make_canonical(sig_bytes))

    # Check the signature is still valid
    ecdsa_pubkey = secp256k1.PublicKey(pubkey=pub_key_bytes, raw=True)
    sig_ser = ecdsa_pubkey.ecdsa_deserialize_compact(sig_bytes)
    verified_ecdsa = ecdsa_pubkey.ecdsa_verify(msg_hash_bytes, sig_ser, raw=True)
    assert verified_ecdsa

    v = -1
    unrelated = MyECDSA()
    for i in range(0, 2):
        recsig = unrelated.ecdsa_recoverable_deserialize(sig_bytes, i)
        pubkey_recovered = unrelated.ecdsa_recover(msg_hash_bytes, recsig, raw=True)
        pubser = secp256k1.PublicKey(pubkey_recovered).serialize(compressed=False)
        if pubser == pub_key_bytes:
            v = i
            break

    assert v == 0 or v == 1

    # // As per the EIP-155 spec, the value of 'v' is also dependent on the chain id.
    # // See: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md#specification
    v += 27

    if chain_id > 0:
        v += chain_id * 2 + 8

    r = sig_bytes[0:32]
    s = sig_bytes[32:64]
    v = v

    return v, int_from_bytes(r), int_from_bytes(s)


def convert_json_key_to_public_key_bytes(json_key):
    pubkey = bytearray()
    pubkey.append(0x04)
    pubkey.extend(json_key.x)
    pubkey.extend(json_key.y)
    pubkey = bytes(pubkey)
    return pubkey


if __name__ == '__main__':
    msg_hash_hex = "e9074b82e0119a67dfd0d35b7dafda9099e6ceb5ae6714dd654b2302084ed4c2"
    pub_key = "0426d9a4764551121fe3b7760a41e563a0bcbe59a52443b819427532afbd3f8ac8e794d705a48fac6cdb64c5453149938d4cca2545ed9fb99ec98b7c13f6680d57"
    sig_hex = "2e8c9d43a1c4d34a44130ed4910e54976bce520e962487b6eb6d4e9def96dda4642936ad51cea9ea7d733ad6dd6674ba52be8069504e1d1e37f402bb72a0bc95"

    msg_hash_bytes = bytes.fromhex(msg_hash_hex)
    pub_key_bytes = bytes.fromhex(pub_key)
    sig_bytes = bytes.fromhex(sig_hex)

    vrs = convert_azure_secp256k1_signature_to_vrs(pub_key_bytes, msg_hash_bytes, sig_bytes)
    print(vrs)
