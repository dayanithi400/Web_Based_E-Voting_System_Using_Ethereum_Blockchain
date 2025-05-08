import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import Candidate

def fix_candidate_ids():
    print("Fixing candidate IDs in the database...")
    
    # Get all candidates
    candidates = Candidate.objects.all()
    print(f"Found {candidates.count()} candidates in the database")
    
    # Update blockchain IDs to match regular IDs
    for candidate in candidates:
        print(f"Candidate: {candidate.name}")
        print(f"  - Current ID: {candidate.id}")
        print(f"  - Current Blockchain ID: {candidate.blockchain_id}")
        
        # Set blockchain_id to match id
        candidate.blockchain_id = candidate.id
        candidate.save()
        
        print(f"  - Updated Blockchain ID: {candidate.blockchain_id}")
        print()
    
    print("Candidate ID fix complete!")

if __name__ == "__main__":
    fix_candidate_ids()
