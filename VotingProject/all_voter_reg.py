import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import User
from VotingProject.utils.web3_utils import Web3Utils
import time

def register_all_voters():
    print("Registering all voters on the blockchain...")
    
    try:
        # Initialize Web3Utils
        web3_utils = Web3Utils()
        print("Web3Utils initialized successfully")
        print(f"Admin account: {web3_utils.admin_account}")
        print(f"Contract address: {web3_utils.contract_address}")
    except Exception as e:
        print(f"Error initializing Web3Utils: {e}")
        return
    
    # Get all users from the database
    users = User.objects.all()
    print(f"Found {users.count()} users in the database")
    
    success_count = 0
    error_count = 0
    
    # First, make sure admin account is registered
    try:
        admin_address = web3_utils.admin_account
        print(f"\nChecking if admin account {admin_address} is registered...")
        
        is_registered = web3_utils.is_registered_voter(admin_address)
        if is_registered:
            print(f"Admin account is already registered")
        else:
            print(f"Registering admin account...")
            tx_receipt = web3_utils.register_voter(admin_address, "ADMIN_VOTER_ID")
            print(f"Admin account registered successfully")
            print(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
            success_count += 1
    except Exception as e:
        print(f"Error registering admin account: {e}")
        error_count += 1
    
    # Now register all other users
    for user in users:
        print(f"\nProcessing user: {user.username} (ID: {user.id})")
        print(f"  - Ethereum address: {user.eth_address}")
        print(f"  - Voter ID: {user.voter_id}")
        
        # Skip if no eth_address or voter_id
        if not user.eth_address or not user.voter_id:
            print(f"  - Skipping: Missing eth_address or voter_id")
            continue
        
        # Check if already registered
        try:
            is_registered = web3_utils.is_registered_voter(user.eth_address)
            if is_registered:
                print(f"  - User is already registered on blockchain")
                user.is_registered_on_blockchain = True
                user.save()
                continue
        except Exception as e:
            print(f"  - Error checking if user is registered: {e}")
        
        # Register user on blockchain
        try:
            print(f"  - Registering user on blockchain...")
            tx_receipt = web3_utils.register_voter(user.eth_address, user.voter_id)
            print(f"  - Successfully registered user on blockchain")
            print(f"  - Transaction hash: {tx_receipt.transactionHash.hex()}")
            
            # Update user in database
            user.is_registered_on_blockchain = True
            user.save()
            
            success_count += 1
            
            # Sleep briefly to avoid overwhelming the blockchain
            time.sleep(1)
        except Exception as e:
            print(f"  - Error registering user on blockchain: {e}")
            error_count += 1
    
    print(f"\nRegistration complete! Successfully registered {success_count} users, {error_count} errors.")

if __name__ == "__main__":
    register_all_voters()