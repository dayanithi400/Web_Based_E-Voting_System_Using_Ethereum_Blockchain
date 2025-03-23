import json
import os
from web3 import Web3

def check_contract_connection():
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    
    # Check if connected to Ethereum node
    if not w3.isConnected():
        print("❌ Failed to connect to Ethereum node.")
        return False
    
    print("✅ Connected to Ethereum node.")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    
    # Load contract info
    contract_info_path = os.path.join(project_dir, 'deployment', 'contract_info.json')
    
    try:
        with open(contract_info_path, 'r') as file:
            contract_info = json.load(file)
            
        contract_address = contract_info['contract_address']
        abi = contract_info['abi']
        admin_account = contract_info['deployer_account']
        
        print(f"✅ Contract info loaded successfully.")
        print(f"   Contract address: {contract_address}")
        print(f"   Admin account: {admin_account}")
        
        # Create contract instance
        contract = w3.eth.contract(
            address=contract_address,
            abi=abi
        )
        
        print(f"✅ Contract instance created successfully.")
        
        # Try to call a function on the contract
        try:
            candidates_count = contract.functions.candidatesCount().call()
            print(f"✅ Contract function call successful.")
            print(f"   Number of candidates: {candidates_count}")
            return True
        except Exception as e:
            print(f"❌ Error calling contract function: {e}")
            return False
            
    except FileNotFoundError:
        print(f"❌ Contract info file not found at {contract_info_path}")
        print("   Please deploy the contract first.")
        return False
    except Exception as e:
        print(f"❌ Error checking contract connection: {e}")
        return False

if __name__ == "__main__":
    check_contract_connection()