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

def fix_voter_id(username):
    try:
        # Connect to Ganache
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        if not w3.isConnected():
            print("Failed to connect to Ganache")
            return False
        
        # Initialize Web3Utils
        web3_utils = Web3Utils()
        
        # Get the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"User '{username}' not found")
            return False
        
        print(f"Found user: {user.username}")
        print(f"  Current Voter ID: {user.voter_id}")
        print(f"  Current ETH Address: {user.eth_address}")
        
        # Option 1: Find the address associated with this voter ID
        try:
            # This function doesn't exist in the original contract, so we'll skip this approach
            # address = web3_utils.contract.functions.voterIdToAddress(user.voter_id).call()
            # print(f"This voter ID is registered to address: {address}")
            pass
        except Exception as e:
            print(f"Could not find address for voter ID: {e}")
        
        # Option 2: Use a new voter ID
        new_voter_id = input("Enter a new voter ID for this user: ")
        
        # Update user's voter ID
        old_voter_id = user.voter_id
        user.voter_id = new_voter_id
        user.is_registered_on_blockchain = False  # Reset this flag
        user.save()
        print(f"Updated user's voter ID from {old_voter_id} to {new_voter_id}")
        
        # Get available Ganache accounts
        ganache_accounts = w3.eth.accounts
        print(f"\nAvailable Ganache accounts:")
        for i, account in enumerate(ganache_accounts):
            print(f"{i+1}. {account}")
        
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
        user.save()
        print(f"Updated user's ETH address from {old_address} to {new_address}")
        
        # Register the user on the blockchain
        print(f"Registering user on blockchain with new voter ID and address...")
        
        # Register on blockchain
        tx_receipt = web3_utils.register_voter(new_address, new_voter_id)
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
        print(f"Error fixing voter ID: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = input("Enter username to fix: ")
    
    fix_voter_id(username)