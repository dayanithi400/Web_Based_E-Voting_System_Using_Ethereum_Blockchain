import os
import sys

# Add the parent directory to the path so we can import the modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.dirname(parent_dir))

from VotingProject.utils.web3_utils import Web3Utils

def register_test_candidate():
    try:
        print("Initializing Web3Utils...")
        web3_utils = Web3Utils()
        
        print("Registering test candidate...")
        candidate_name = "Test Candidate"
        candidate_area = "Test Area"
        
        tx_receipt = web3_utils.register_candidate(candidate_name, candidate_area)
        
        print(f"Candidate registered successfully!")
        print(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
        
        # Try to get the candidate ID from the event logs
        try:
            logs = web3_utils.contract.events.CandidateRegistered().process_receipt(tx_receipt)
            candidate_id = logs[0]['args']['id']
            print(f"Candidate ID: {candidate_id}")
        except Exception as e:
            print(f"Could not get candidate ID from logs: {e}")
        
        return True
    except Exception as e:
        print(f"Error registering candidate: {e}")
        return False

if __name__ == "__main__":
    register_test_candidate()