# signing-azure-keyvault-secp256k1-ethereum
step by step tutorial to sign ethereum transaction using azure keyvault and python3


# Dependencies

Ubuntu:

```
sudo apt-get install build-essential automake libtool pkg-config libffi-dev python-dev python-pip libsecp256k1-dev
```

MacOS:

```bash
brew install openssl libtool pkg-config automake
export LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include"
```

Python 3:

```
pip install -r requirements.txt
```

## Create a Service Principal that would have access to your key

https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest

## Create a Key Vault

Login on the Azure Portal ( https://portal.azure.com/ )

- Go to `Key Vaults`

![Keyvault search](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/1-keyvault.png)

- Create a new Keyvault

![Create Keyvault](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/2-create-keyvault.png)

- Set up policies of your keyvault to the Service Principal

![Setup Keyvault Policies](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/3-create-keyvault-policies.png)

## Create a SECP256K1 Key

- Go to your keyvault

![Your Key Vault](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/4-hsm-keys.png)

- Create a new key and select SECP256k1 options

![Create a key](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/5-create-a-key.png)

- Done

![Key Details](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/6-key-details-id.png)


## Create config.py

Copy the contents of `config.py.sample` to a new file named `config.py` and fill it with your secrets


Your service principal credentials:

- `CLIENT_ID` is a UUID
- `PASSWORD` is the password

The Vault details:

- `TENANT_ID` is the directory ID, available in the keyvault overview
- `VAULT_URL` is the Vault link, available in the keyvault overview as `DNS Name`

![Key Vault](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/1-config-py.png)


The Key details:

- `KEY_NAME` is the key name
- `KEY_VERSION` is the key version

![Key Vault](https://raw.githubusercontent.com/davidp94/signing-azure-keyvault-secp256k1-ethereum/master/static/2-config-py.png)

## Run the example

Run a ganache-cli instance
```
ganache-cli
```

Makes sure that the address has enough balance.

You might need to change the nonce manually (in the example.py) or replace it with `getTransactionCount` ( https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.getTransactionCount )

```
python3 example.py
```