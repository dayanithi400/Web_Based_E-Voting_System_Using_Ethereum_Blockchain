import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingProject.utils.web3_utils import Web3Utils

def check_blockchain_candidates():
    try:
        web3_utils = Web3Utils()
        
        # Get total candidates on blockchain
        candidates_count = web3_utils.contract.functions.candidatesCount().call()
        print(f"Total candidates on blockchain: {candidates_count}")
        
        # List all candidates on blockchain
        if candidates_count > 0:
            print("\nCandidates on blockchain:")
            for i in range(1, candidates_count + 1):
                try:
                    candidate = web3_utils.get_candidate(i)
                    print(f"ID: {candidate[0]}, Name: {candidate[1]}, Area: {candidate[2]}, Votes: {candidate[3]}")
                except Exception as e:
                    print(f"Error getting candidate {i}: {e}")
        else:
            print("No candidates on blockchain")
    
    except Exception as e:
        print(f"Error checking blockchain candidates: {e}")

if __name__ == "__main__":
    check_blockchain_candidates()