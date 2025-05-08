import os
import django
import sys
import json
from web3 import Web3

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import User

class Web3UtilsSimple:
    def __init__(self):
        # Connect to Ethereum node
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Ganache default
        
        # Check if connected
        if not self.w3.isConnected():
            raise Exception("Failed to connect to Ethereum node")
        
        # Set default account (first account in Ganache)
        self.admin_account = self.w3.eth.accounts[0]
        
        # Find contract_data.json
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        possible_paths = [
            os.path.join(project_root, 'contracts', 'contract_data.json'),
            os.path.join(project_root, 'VotingProject', 'contracts', 'contract_data.json'),
            os.path.join(project_root, 'utils', 'contract_data.json'),
            os.path.join(project_root, 'VotingProject', 'utils', 'contract_data.json')
        ]
        
        contract_path = None
        for path in possible_paths:
            if os.path.exists(path):
                contract_path = path
                break
        
        if not contract_path:
            raise Exception("Could not find contract_data.json file")
        
        print(f"Using contract data from: {contract_path}")
        
        # Load contract data
        with open(contract_path, 'r') as file:
            contract_data = json.load(file)
        
        # Get contract ABI and address
        self.contract_address = contract_data['address']
        self.contract_abi = contract_data['abi']
        
        # Create contract instance
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)
    
    def register_voter(self, voter_address, voter_id):
        """
        Register a voter on the blockchain.
        """
        # In development, we'll use the admin account for all transactions
        tx_hash = self.contract.functions.registerVoter(voter_address, voter_id).transact({
            'from': self.admin_account,
            'gas': 3000000
        })
        
        # Wait for the transaction to be mined
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def is_registered_voter(self, address):
        """
        Check if a voter is registered.
        """
        try:
            return self.contract.functions.isRegisteredVoter(address).call()
        except Exception as e:
            print(f"Error checking if voter is registered: {e}")
            return False

def register_all_voters():
    print("Registering all voters on the blockchain...")
    
    try:
        # Initialize Web3Utils
        web3_utils = Web3UtilsSimple()
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
            import time
            time.sleep(1)
        except Exception as e:
            print(f"  - Error registering user on blockchain: {e}")
            error_count += 1
    
    print(f"\nRegistration complete! Successfully registered {success_count} users, {error_count} errors.")

if __name__ == "__main__":
    register_all_voters()