import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import User
from VotingProject.utils.web3_utils import Web3Utils
from web3 import Web3

def fix_user_address(username):
    try:
        # Connect to Ganache
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        if not w3.isConnected():
            print("Failed to connect to Ganache")
            return False
        
        # Get available Ganache accounts
        ganache_accounts = w3.eth.accounts
        print(f"Available Ganache accounts:")
        for i, account in enumerate(ganache_accounts):
            print(f"{i+1}. {account}")
        
        # Get the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"User '{username}' not found")
            return False
        
        print(f"\nFound user: {user.username}")
        print(f"  Current ETH Address: {user.eth_address}")
        
        # Choose a Ganache account to use
        account_index = int(input("\nEnter the number of the account to use (1-10): ")) - 1
        if account_index < 0 or account_index >= len(ganache_accounts):
            print("Invalid account number")
            return False
        
        new_address = ganache_accounts[account_index]
        print(f"Selected account: {new_address}")
        
        # Update user's Ethereum address
        old_address = user.eth_address
        user.eth_address = new_address
        user.is_registered_on_blockchain = False  # Reset this flag
        user.save()
        print(f"Updated user's ETH address from {old_address} to {new_address}")
        
        # Register the user on the blockchain
        web3_utils = Web3Utils()
        print(f"Registering user on blockchain...")
        
        # Make sure voter_id is not empty
        if not user.voter_id:
            voter_id = input("User has no voter ID. Enter a voter ID: ")
            user.voter_id = voter_id
            user.save()
            print(f"Updated user with voter ID: {voter_id}")
        
        # Register on blockchain
        tx_receipt = web3_utils.register_voter(new_address, user.voter_id)
        print(f"User registered on blockchain successfully!")
        print(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
        
        # Update the user in the database
        user.is_registered_on_blockchain = True
        user.save()
        print(f"User database record updated")
        
        # Verify registration
        is_registered = web3_utils.is_registered_voter(new_address)
        print(f"Verification - Is registered on blockchain: {is_registered}")
        
        print("\nNow you should be able to vote successfully!")
        return True
    except Exception as e:
        print(f"Error fixing user address: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter username to fix: ")
    
    fix_user_address(username)