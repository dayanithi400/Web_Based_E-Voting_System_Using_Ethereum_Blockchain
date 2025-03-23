import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import User
from VotingProject.utils.web3_utils import Web3Utils

def check_user_addresses():
    try:
        web3_utils = Web3Utils()
        
        # Get all users
        users = User.objects.all()
        
        print(f"Found {len(users)} users")
        
        for user in users:
            print(f"User: {user.username}")
            print(f"  Voter ID: {user.voter_id}")
            print(f"  ETH Address: {user.eth_address}")
            
            if user.eth_address:
                # Check if the user is registered on the blockchain
                try:
                    is_registered = web3_utils.is_registered_voter(user.eth_address)
                    print(f"  Registered on blockchain: {is_registered}")
                    
                    if not is_registered and user.is_registered_on_blockchain:
                        print(f"  WARNING: User is marked as registered in database but not on blockchain")
                        
                        # Register the user on the blockchain
                        print(f"  Registering user on blockchain...")
                        tx_receipt = web3_utils.register_voter(user.eth_address, user.voter_id)
                        print(f"  User registered on blockchain. TX: {tx_receipt.transactionHash.hex()}")
                        
                        user.is_registered_on_blockchain = True
                        user.save()
                except Exception as e:
                    print(f"  Error checking registration: {e}")
            else:
                print(f"  WARNING: User has no ETH address")
                
                # Create a new ETH address for the user
                try:
                    eth_address, _ = web3_utils.get_new_account()
                    print(f"  Created new ETH address: {eth_address}")
                    
                    user.eth_address = eth_address
                    user.save()
                    
                    # Register the user on the blockchain
                    print(f"  Registering user on blockchain...")
                    tx_receipt = web3_utils.register_voter(eth_address, user.voter_id)
                    print(f"  User registered on blockchain. TX: {tx_receipt.transactionHash.hex()}")
                    
                    user.is_registered_on_blockchain = True
                    user.save()
                except Exception as e:
                    print(f"  Error creating/registering address: {e}")
            
            print("")
        
        return True
    except Exception as e:
        print(f"Error checking user addresses: {e}")
        return False

if __name__ == "__main__":
    check_user_addresses()