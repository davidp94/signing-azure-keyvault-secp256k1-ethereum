from eth_keys import KeyAPI

def public_key_to_address(public_key):
    return KeyAPI.PublicKey(public_key_bytes=public_key).to_checksum_address()