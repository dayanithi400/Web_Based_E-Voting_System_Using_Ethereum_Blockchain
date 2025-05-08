import os
import django
import sys
import json
from web3 import Web3

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import Candidate
from django.conf import settings

def register_candidates_in_blockchain():
    print("Registering candidates in the blockchain...")
    
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Default Ganache URL
    
    if not w3.isConnected():
        print("Error: Could not connect to Ganache. Make sure it's running.")
        return
    
    print(f"Connected to Ganache: {w3.isConnected()}")
    
    # Get the contract ABI and address
    try:
        # Try to get from settings if available
        contract_address = getattr(settings, 'CONTRACT_ADDRESS', None)
        contract_abi_path = getattr(settings, 'CONTRACT_ABI_PATH', None)
        
        # If not in settings, use default locations
        if not contract_address:
            # Look for contract address in a file
            try:
                with open('contract_address.txt', 'r') as f:
                    contract_address = f.read().strip()
            except FileNotFoundError:
                print("Contract address not found. Please enter it:")
                contract_address = input().strip()
        
        if not contract_abi_path:
            # Try common locations for ABI
            possible_paths = [
                'contract_abi.json',
                'VotingApp/static/contract_abi.json',
                'VotingApp/contract_abi.json',
                'static/contract_abi.json'
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    contract_abi_path = path
                    break
            
            if not contract_abi_path:
                print("Contract ABI file not found. Please enter the path:")
                contract_abi_path = input().strip()
        
        # Load ABI
        with open(contract_abi_path, 'r') as f:
            contract_abi = json.load(f)
        
        print(f"Using contract at address: {contract_address}")
    except Exception as e:
        print(f"Error loading contract information: {e}")
        print("Please enter contract ABI manually (as JSON):")
        contract_abi = json.loads(input().strip())
        print("Please enter contract address:")
        contract_address = input().strip()
    
    # Get contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    # Get accounts
    accounts = w3.eth.accounts
    if not accounts:
        print("No accounts found in Ganache")
        return
    
    admin_account = accounts[0]  # Use the first account as admin
    print(f"Using admin account: {admin_account}")
    
    # Get all candidates
    candidates = Candidate.objects.all()
    print(f"Found {candidates.count()} candidates in the database")
    
    # Register each candidate in the blockchain
    for candidate in candidates:
        print(f"Registering candidate: {candidate.name}")
        print(f"  - ID: {candidate.id}")
        print(f"  - Blockchain ID: {candidate.blockchain_id}")
        
        try:
            # Check if candidate already exists in blockchain
            try:
                candidate_exists = contract.functions.getVoteCount(candidate.blockchain_id).call({'from': admin_account})
                print(f"  - Candidate already exists in blockchain with ID {candidate.blockchain_id}")
                continue
            except Exception:
                # Candidate doesn't exist, proceed with registration
                pass
            
            # Register the candidate
            tx_hash = contract.functions.addCandidate(
                candidate.blockchain_id,
                candidate.name
            ).transact({'from': admin_account})
            
            # Wait for transaction receipt
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"  - Successfully registered in blockchain. Transaction hash: {tx_hash.hex()}")
            
            # Verify registration
            vote_count = contract.functions.getVoteCount(candidate.blockchain_id).call({'from': admin_account})
            print(f"  - Verified: Candidate has {vote_count} votes")
            
        except Exception as e:
            print(f"  - Error registering candidate: {e}")
        
        print()
    
    print("Candidate registration complete!")

if __name__ == "__main__":
    register_candidates_in_blockchain()
