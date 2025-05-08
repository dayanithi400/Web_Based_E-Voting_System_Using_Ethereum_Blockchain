import json
import os
from web3 import Web3

def check_blockchain_connection():
    print("Checking blockchain connection...")
    
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Default Ganache URL
    
    if not w3.isConnected():
        print("Error: Could not connect to Ganache. Make sure it's running.")
        return
    
    print(f"Connected to Ganache: {w3.isConnected()}")
    
    # Get accounts
    accounts = w3.eth.accounts
    print(f"Available accounts: {len(accounts)}")
    for i, account in enumerate(accounts):
        balance = w3.eth.get_balance(account)
        print(f"  Account {i}: {account}")
        print(f"    Balance: {w3.fromWei(balance, 'ether')} ETH")
    
    # Try to get contract information
    try:
        # Look for contract address in a file
        if os.path.exists('contract_address.txt'):
            with open('contract_address.txt', 'r') as f:
                contract_address = f.read().strip()
                print(f"Found contract address: {contract_address}")
        
        # Look for ABI in common locations
        abi_paths = [
            'contract_abi.json',
            'VotingApp/static/contract_abi.json',
            'VotingApp/contract_abi.json',
            'static/contract_abi.json'
        ]
        
        for path in abi_paths:
            if os.path.exists(path):
                print(f"Found contract ABI at: {path}")
                with open(path, 'r') as f:
                    contract_abi = json.load(f)
                print(f"ABI contains {len(contract_abi)} entries")
                break
    except Exception as e:
        print(f"Error checking contract information: {e}")
    
    print("Blockchain connection check complete!")

if __name__ == "__main__":
    check_blockchain_connection()
