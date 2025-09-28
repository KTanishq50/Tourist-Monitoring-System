# services/blockchain.py
import os
import json
from web3 import Web3
from hashlib import sha256

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(BASE_DIR, "build")
DEPLOYED_JSON = os.path.join(BUILD_DIR, "TouristRegistry_deployed.json")
RPC = os.environ.get("GANACHE_RPC", "http://127.0.0.1:8545")

w3 = Web3(Web3.HTTPProvider(RPC))
if not w3.is_connected():
    print(" web3 not connected to", RPC)

_contract = None
def _load_contract():
    global _contract
    if _contract is not None:
        return _contract

    if not os.path.exists(DEPLOYED_JSON):
        raise FileNotFoundError("Compiled/deployed contract JSON missing. compiled first " + DEPLOYED_JSON)

    with open(DEPLOYED_JSON, "r", encoding="utf-8") as f:
        js = json.load(f)
    abi = js["abi"]
    address = js["address"]
    _contract = w3.eth.contract(address=address, abi=abi)
    return _contract

def hash_sensitive(s: str) -> str:
    """Hash Aadhaar/PAN before storing on chain."""
    return sha256(s.encode("utf-8")).hexdigest()

def add_tourist(tourist_id, name, aadhaar_plain, valid_from_ts, valid_to_ts):
    
    contract = _load_contract()
    acct = w3.eth.accounts[0]  # authority account 
    aadhaar_hash = hash_sensitive(aadhaar_plain)
    tx_hash = contract.functions.addTourist(
        str(tourist_id),
        str(name),
        str(aadhaar_hash),
        int(valid_from_ts),
        int(valid_to_ts)
        
    ).transact({"from": acct})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()

def get_tourist(tid):
    contract = _load_contract()
    
    return contract.functions.getTourist(str(tid)).call()

def get_all_tourists():
    contract = _load_contract()
    return contract.functions.getAllTourists().call()
