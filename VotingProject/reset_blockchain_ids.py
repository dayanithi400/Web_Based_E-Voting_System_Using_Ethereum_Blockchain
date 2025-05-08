import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import Candidate

def reset_blockchain_ids():
    print("Resetting blockchain IDs in the database...")
    
    # Get all candidates
    candidates = Candidate.objects.all()
    print(f"Found {candidates.count()} candidates in the database")
    
    # Reset blockchain IDs to 1-based index
    for i, candidate in enumerate(candidates, 1):
        print(f"Candidate: {candidate.name}")
        print(f"  - Current ID: {candidate.id}")
        print(f"  - Current Blockchain ID: {candidate.blockchain_id}")
        
        # Set blockchain_id to sequential number starting from 1
        candidate.blockchain_id = i
        candidate.save()
        
        print(f"  - Updated Blockchain ID: {candidate.blockchain_id}")
        print()
    
    print("Blockchain ID reset complete!")

if __name__ == "__main__":
    reset_blockchain_ids()
