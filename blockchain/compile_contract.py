# blockchain/compile_contract.py
import json
import os
from solcx import install_solc, set_solc_version, compile_standard

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRACTS_DIR = os.path.join(BASE_DIR, "contracts")
BUILD_DIR = os.path.join(BASE_DIR, "build")
os.makedirs(BUILD_DIR, exist_ok=True)


SOLC_VERSION = "0.8.20"
install_solc(SOLC_VERSION)
set_solc_version(SOLC_VERSION)

# Read contract
with open(os.path.join(CONTRACTS_DIR, "TouristRegistry.sol"), "r", encoding="utf-8") as f:
    source = f.read()

# Compile contract
compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "TouristRegistry.sol": {"content": source}
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        },
    },
    allow_paths=CONTRACTS_DIR,
)


out_path = os.path.join(BUILD_DIR, "TouristRegistry.json")
with open(out_path, "w", encoding="utf-8") as out_f:
    json.dump(compiled, out_f, indent=2)

print("Full contract JSON saved to:", out_path)
