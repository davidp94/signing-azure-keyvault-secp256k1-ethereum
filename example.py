from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials

from config import CLIENT_ID, PASSWORD, TENANT_ID, VAULT_URL, KEY_NAME, KEY_VERSION

from ethtoken.abi import EIP20_ABI
from web3 import Web3, HTTPProvider

from eth_account.internal.transactions import serializable_unsigned_transaction_from_dict, encode_transaction

from azure_utils import convert_azure_secp256k1_signature_to_vrs, convert_json_key_to_public_key_bytes

from utils import public_key_to_address


def sign_keyvault(client, vault_url, key_name, key_version, unsigned_tx_hash, chain_id=0):
    key_bundle = client.get_key(vault_url, key_name, key_version)
    json_key = key_bundle.key
    pubkey = convert_json_key_to_public_key_bytes(json_key)
    address_signer = public_key_to_address(pubkey[1:])

    sig_resp = client.sign(vault_url, key_name, key_version, 'ECDSA256', unsigned_tx_hash)

    vrs = convert_azure_secp256k1_signature_to_vrs(pubkey, unsigned_tx_hash, sig_resp.result, chain_id)

    ret_signed_transaction = encode_transaction(unsigned_tx, vrs)
    return address_signer, ret_signed_transaction


def auth_callback(server, resource, scope):
    credentials = ServicePrincipalCredentials(
        client_id=CLIENT_ID,
        secret=PASSWORD,
        tenant=TENANT_ID,
        resource='https://vault.azure.net'
    )
    token = credentials.token
    return token['token_type'], token['access_token']


client = KeyVaultClient(KeyVaultAuthentication(auth_callback))

w3 = Web3(HTTPProvider('http://localhost:8545'))

unicorns = w3.eth.contract(address="0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359", abi=EIP20_ABI)

unicorn_txn = unicorns.functions.transfer(
    '0xfB6916095ca1df60bB79Ce92cE3Ea74c37c5d359',
    1,
).buildTransaction({
    'gas': 70000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'nonce': 0,
})

unsigned_tx = serializable_unsigned_transaction_from_dict(unicorn_txn)

unsigned_tx_hash = unsigned_tx.hash()

address_signer, signed_transaction = sign_keyvault(client, VAULT_URL, KEY_NAME, KEY_VERSION, unsigned_tx_hash)

print("Signer", address_signer)
print("Signed Tx", signed_transaction.hex())

tx_hash = w3.eth.sendRawTransaction(signed_transaction.hex())

print("tx hash", tx_hash.hex())
