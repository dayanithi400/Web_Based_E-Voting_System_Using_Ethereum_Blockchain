import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import Candidate

def check_candidate_ids():
    print("Checking candidate IDs in the database...")
    
    # Get all candidates
    candidates = Candidate.objects.all()
    print(f"Found {candidates.count()} candidates in the database")
    
    # Check IDs of each candidate
    for candidate in candidates:
        print(f"Candidate: {candidate.name}")
        print(f"  - ID: {candidate.id}")
        print(f"  - Blockchain ID: {candidate.blockchain_id}")
        print(f"  - Area: {candidate.area}")
        print(f"  - Party: {candidate.party}")
        print()
    
    print("Candidate ID check complete!")

if __name__ == "__main__":
    check_candidate_ids()
