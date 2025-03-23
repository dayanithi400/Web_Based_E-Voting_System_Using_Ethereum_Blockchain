import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import Candidate
from VotingProject.utils.web3_utils import Web3Utils

def check_candidates():
    try:
        web3_utils = Web3Utils()
        
        # Get all candidates from database
        candidates = Candidate.objects.all()
        print(f"Found {len(candidates)} candidates in database")
        
        for candidate in candidates:
            print(f"Checking candidate: {candidate.name} (ID: {candidate.blockchain_id})")
            
            # Check if candidate exists on blockchain
            try:
                blockchain_candidate = web3_utils.get_candidate(candidate.blockchain_id)
                print(f"  ✅ Exists on blockchain: {blockchain_candidate}")
            except Exception as e:
                print(f"  ❌ Does not exist on blockchain: {e}")
                
                # Ask if user wants to delete this candidate
                delete = input(f"  Delete candidate {candidate.name} from database? (y/n): ")
                if delete.lower() == 'y':
                    candidate.delete()
                    print(f"  Deleted candidate {candidate.name} from database")
        
        # Check total candidates on blockchain
        try:
            candidates_count = web3_utils.contract.functions.candidatesCount().call()
            print(f"\nTotal candidates on blockchain: {candidates_count}")
            
            # Check if there are candidates on blockchain not in database
            for i in range(1, candidates_count + 1):
                try:
                    # Check if candidate exists in database
                    candidate = Candidate.objects.filter(blockchain_id=i).first()
                    if not candidate:
                        # Get candidate from blockchain
                        blockchain_candidate = web3_utils.get_candidate(i)
                        print(f"Candidate ID {i} exists on blockchain but not in database:")
                        print(f"  Name: {blockchain_candidate[1]}")
                        print(f"  Area: {blockchain_candidate[2]}")
                        
                        # Ask if user wants to add this candidate to database
                        add = input(f"  Add candidate {blockchain_candidate[1]} to database? (y/n): ")
                        if add.lower() == 'y':
                            Candidate.objects.create(
                                name=blockchain_candidate[1],
                                area=blockchain_candidate[2],
                                blockchain_id=i
                            )
                            print(f"  Added candidate {blockchain_candidate[1]} to database")
                except Exception as e:
                    print(f"Error checking candidate ID {i} on blockchain: {e}")
        except Exception as e:
            print(f"Error getting total candidates on blockchain: {e}")
        
    except Exception as e:
        print(f"Error checking candidates: {e}")

if __name__ == "__main__":
    check_candidates()