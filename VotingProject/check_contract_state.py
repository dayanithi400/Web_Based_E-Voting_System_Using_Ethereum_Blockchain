import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import Candidate
from VotingProject.utils.web3_utils import Web3Utils
import time

def register_candidates_on_blockchain():
    print("Registering candidates on the blockchain...")
    
    try:
        # Initialize Web3Utils
        web3_utils = Web3Utils()
        print("Web3Utils initialized successfully")
        print(f"Admin account: {web3_utils.admin_account}")
        print(f"Contract address: {web3_utils.contract_address}")
    except Exception as e:
        print(f"Error initializing Web3Utils: {e}")
        return
    
    # Get all candidates from the database
    candidates = Candidate.objects.all()
    print(f"Found {candidates.count()} candidates in the database")
    
    success_count = 0
    error_count = 0
    
    for candidate in candidates:
        print(f"\nProcessing candidate: {candidate.name} (ID: {candidate.id})")
        print(f"  - Blockchain ID: {candidate.blockchain_id}")
        print(f"  - Area: {candidate.area}")
        print(f"  - Party: {candidate.party}")
        
        # Register candidate on blockchain
        try:
            print(f"  - Registering candidate on blockchain...")
            tx_receipt = web3_utils.register_candidate(candidate.name, candidate.area)
            print(f"  - Successfully registered candidate on blockchain")
            print(f"  - Transaction hash: {tx_receipt.transactionHash.hex()}")
            success_count += 1
            
            # Sleep briefly to avoid overwhelming the blockchain
            time.sleep(1)
        except Exception as e:
            print(f"  - Error registering candidate on blockchain: {e}")
            error_count += 1
    
    print(f"\nRegistration complete! Successfully registered {success_count} candidates, {error_count} errors.")

if __name__ == "__main__":
    register_candidates_on_blockchain()