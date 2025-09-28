# blockchain/deploy_contract.py
import json
import os
from web3 import Web3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BASE_DIR, "build")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load compiled contract
with open(os.path.join(BUILD_DIR, "TouristRegistry.json")) as f:
    compiled = json.load(f)


contract_interface = compiled["contracts"]["TouristRegistry.sol"]["TouristRegistry"]

abi = contract_interface["abi"]
bytecode = contract_interface["evm"]["bytecode"]["object"]

# Using first Ganache account to deploy
account = w3.eth.accounts[0]

TouristRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = TouristRegistry.constructor().transact({"from": account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# saving ABI and deployed address together
deployed = {
    "abi": abi,
    "address": tx_receipt.contractAddress
}

with open(os.path.join(BUILD_DIR, "TouristRegistry_deployed.json"), "w") as f:
    json.dump(deployed, f, indent=2)

print("Contract deployed at:", tx_receipt.contractAddress)
print("ABI and address saved to TouristRegistry_deployed.json")
