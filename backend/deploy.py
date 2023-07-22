from eth_utils import address
from web3 import Web3
import os
from solcx import compile_standard, install_solc
from dotenv import load_dotenv
import json
from dotenv import load_dotenv

install_solc("0.8.6")

with open("./ImageRepository.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ImageRepository.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.6",
)

with open("compiled.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["ImageRepository.sol"]["ImageRepository"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["ImageRepository.sol"]["ImageRepository"]["metadata"]
)["output"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))

load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
address = os.getenv("ADDRESS")

# initialize contract
ImageRepository = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(address)
# set up transaction from constructor which executes when firstly
transaction = ImageRepository.constructor().build_transaction(
    {"from": address, "nonce": nonce}
)
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
