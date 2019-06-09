from azure_utils import make_canonical, convert_json_key_to_public_key_bytes, convert_azure_secp256k1_signature_to_vrs, int_to_bytes


def test_make_canonical():
    sig_hex = "2e8c9d43a1c4d34a44130ed4910e54976bce520e962487b6eb6d4e9def96dda4642936ad51cea9ea7d733ad6dd6674ba52be8069504e1d1e37f402bb72a0bc95"
    sig_bytes = bytes.fromhex(sig_hex)

    sig = make_canonical(sig_bytes)

    print(sig.hex())

    assert sig.hex() == "2e8c9d43a1c4d34a44130ed4910e54976bce520e962487b6eb6d4e9def96dda4642936ad51cea9ea7d733ad6dd6674ba52be8069504e1d1e37f402bb72a0bc95"


class JSONKey(object):
    pass


def test_json_key_to_public_key_bytes():
    json_key = JSONKey()
    json_key.x = bytes.fromhex('26d9a4764551121fe3b7760a41e563a0bcbe59a52443b819427532afbd3f8ac8')
    json_key.y = bytes.fromhex('e794d705a48fac6cdb64c5453149938d4cca2545ed9fb99ec98b7c13f6680d57')

    public_key_bytes = convert_json_key_to_public_key_bytes(json_key)

    assert public_key_bytes.hex() == "0426d9a4764551121fe3b7760a41e563a0bcbe59a52443b819427532afbd3f8ac8e794d705a48fac6cdb64c5453149938d4cca2545ed9fb99ec98b7c13f6680d57"


def test_sig_to_vrs():
    pubkey_bytes = bytes.fromhex("0426d9a4764551121fe3b7760a41e563a0bcbe59a52443b819427532afbd3f8ac8e794d705a48fac6cdb64c5453149938d4cca2545ed9fb99ec98b7c13f6680d57")
    msg_hash_bytes = bytes.fromhex("e9074b82e0119a67dfd0d35b7dafda9099e6ceb5ae6714dd654b2302084ed4c2")
    sig_bytes = bytes.fromhex(
        "2e8c9d43a1c4d34a44130ed4910e54976bce520e962487b6eb6d4e9def96dda4642936ad51cea9ea7d733ad6dd6674ba52be8069504e1d1e37f402bb72a0bc95")

    v, r, s = convert_azure_secp256k1_signature_to_vrs(pub_key_bytes=pubkey_bytes, msg_hash_bytes=msg_hash_bytes,
                                             sig_bytes=sig_bytes)

    assert int_to_bytes(v).hex() == "1b"
    assert int_to_bytes(r).hex() == "2e8c9d43a1c4d34a44130ed4910e54976bce520e962487b6eb6d4e9def96dda4"
    assert int_to_bytes(s).hex() == "642936ad51cea9ea7d733ad6dd6674ba52be8069504e1d1e37f402bb72a0bc95"