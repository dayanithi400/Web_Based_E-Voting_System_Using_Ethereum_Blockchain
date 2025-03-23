import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import User
from VotingProject.utils.web3_utils import Web3Utils

def register_existing_user(username):
    try:
        # Initialize Web3Utils
        web3_utils = Web3Utils()
        
        # Get the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"User '{username}' not found")
            return False
        
        print(f"Found user: {user.username}")
        print(f"  Voter ID: {user.voter_id}")
        print(f"  ETH Address: {user.eth_address}")
        
        if not user.eth_address:
            print(f"User has no ETH address. Creating one...")
            eth_address, _ = web3_utils.get_new_account()
            user.eth_address = eth_address
            user.save()
            print(f"Created new ETH address: {eth_address}")
        
        # Check if already registered
        is_registered = web3_utils.is_registered_voter(user.eth_address)
        print(f"Is registered on blockchain: {is_registered}")
        
        if is_registered:
            print("User is already registered on the blockchain")
            user.is_registered_on_blockchain = True
            user.save()
            return True
        
        # Register the user on the blockchain
        print(f"Registering user on blockchain...")
        tx_receipt = web3_utils.register_voter(user.eth_address, user.voter_id)
        print(f"User registered on blockchain successfully!")
        print(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
        
        # Update the user in the database
        user.is_registered_on_blockchain = True
        user.save()
        print(f"User database record updated")
        
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter username to register: ")
    
    register_existing_user(username)