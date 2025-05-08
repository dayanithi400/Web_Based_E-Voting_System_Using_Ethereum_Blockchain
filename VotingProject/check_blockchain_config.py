import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from django.conf import settings
import json
from web3 import Web3

def check_blockchain_config():
    print("Checking blockchain configuration...")
    
    # Check if blockchain settings are configured
    provider_url = getattr(settings, 'BLOCKCHAIN_PROVIDER_URL', None)
    contract_address = getattr(settings, 'CONTRACT_ADDRESS', None)
    contract_abi_path = getattr(settings, 'CONTRACT_ABI_PATH', None)
    admin_address = getattr(settings, 'ADMIN_ADDRESS', None)
    admin_private_key = getattr(settings, 'ADMIN_PRIVATE_KEY', None)
    
    print(f"BLOCKCHAIN_PROVIDER_URL: {provider_url}")
    print(f"CONTRACT_ADDRESS: {contract_address}")
    print(f"CONTRACT_ABI_PATH: {contract_abi_path}")
    print(f"ADMIN_ADDRESS: {admin_address}")
    print(f"ADMIN_PRIVATE_KEY: {'Configured' if admin_private_key else 'Not configured'}")
    
    if not provider_url:
        print("ERROR: BLOCKCHAIN_PROVIDER_URL is not configured")
        return
    
    if not contract_address:
        print("ERROR: CONTRACT_ADDRESS is not configured")
        return
    
    if not contract_abi_path:
        print("ERROR: CONTRACT_ABI_PATH is not configured")
        return
    
    if not admin_address:
        print("ERROR: ADMIN_ADDRESS is not configured")
        return
    
    if not admin_private_key:
        print("ERROR: ADMIN_PRIVATE_KEY is not configured")
        return
    
    # Check if contract ABI file exists
    if not os.path.exists(contract_abi_path):
        print(f"ERROR: Contract ABI file not found at {contract_abi_path}")
        return
    
    # Load contract ABI
    try:
        with open(contract_abi_path, 'r') as f:
            contract_abi = json.load(f)
        print("Contract ABI loaded successfully")
    except Exception as e:
        print(f"ERROR: Failed to load contract ABI: {e}")
        return
    
    # Connect to Ethereum node
    try:
        w3 = Web3(Web3.HTTPProvider(provider_url))
        if not w3.is_connected():
            print(f"ERROR: Failed to connect to Ethereum node at {provider_url}")
            return
        print(f"Connected to Ethereum node: {provider_url}")
    except Exception as e:
        print(f"ERROR: Failed to connect to Ethereum node: {e}")
        return
    
    # Check if admin address is valid
    try:
        admin_checksum = w3.to_checksum_address(admin_address)
        print(f"Admin address is valid: {admin_checksum}")
    except Exception as e:
        print(f"ERROR: Invalid admin address: {e}")
        return
    
    # Check admin account balance
    try:
        balance = w3.eth.get_balance(admin_checksum)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"Admin account balance: {balance_eth} ETH")
        
        if balance == 0:
            print("WARNING: Admin account has zero balance")
    except Exception as e:
        print(f"ERROR: Failed to get admin account balance: {e}")
        return
    
    # Check if contract exists
    try:
        contract = w3.eth.contract(
            address=w3.to_checksum_address(contract_address),
            abi=contract_abi
        )
        print(f"Contract loaded at address: {contract_address}")
    except Exception as e:
        print(f"ERROR: Failed to load contract: {e}")
        return
    
    # Try to call a read-only function
    try:
        # Assuming the contract has a candidateCount function
        candidate_count = contract.functions.candidateCount().call()
        print(f"Contract candidateCount: {candidate_count}")
    except Exception as e:
        print(f"ERROR: Failed to call contract function: {e}")
        return
    
    print("\nBlockchain configuration check complete!")
    print("If you're still having issues, try the following:")
    print("1. Make sure your Ganache instance is running")
    print("2. Make sure the contract is deployed to the correct address")
    print("3. Make sure the admin account is funded with ETH")
    print("4. Make sure the admin private key is correct")

if __name__ == "__main__":
    check_blockchain_config()