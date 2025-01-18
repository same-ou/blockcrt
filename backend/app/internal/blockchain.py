import json 
import os 
from pathlib import Path
from web3 import Web3


# Load environment variables
BLOCKCHAIN_NODE_URL = os.getenv("BLOCKCHAIN_NODE_URL", "http://127.0.0.1:8545")
CONTRACT_ABI_PATH = os.getenv("CONTRACT_ABI_PATH", "../build/contracts/Certification.json")
DEPLOYMENT_CONFIG_PATH = os.getenv("DEPLOYMENT_CONFIG_PATH", "./deployment_config.json")

# Connect to an Ethereum node
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_NODE_URL))

# Load the contract ABI
def get_contract_abi():
    certification_json_path = Path(CONTRACT_ABI_PATH)

    try:
        with open(certification_json_path, "r") as json_file:
            certification_data = json.load(json_file)
            return certification_data.get("abi", [])
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {certification_json_path} not found.")

# Load the ABI and contract
contract_abi = get_contract_abi()


deployment_config_fpath = Path(DEPLOYMENT_CONFIG_PATH)
with open(deployment_config_fpath, 'r') as json_file:
    address_data = json.load(json_file)
contract_address = address_data.get('Certification')

contract = w3.eth.contract(address=contract_address, abi=contract_abi)