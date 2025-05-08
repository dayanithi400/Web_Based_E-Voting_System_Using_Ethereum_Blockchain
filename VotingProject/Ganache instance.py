import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from web3 import Web3

def check_ganache_accounts():
    print("Checking Ganache accounts...")
    
    try:
        # Connect to Ganache
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Check if connected
        if not w3.isConnected():
            print("Failed to connect to Ethereum node.")
            return
        
        print("Connected to Ethereum node.")
        
        # Get accounts
        accounts = w3.eth.accounts
        print(f"Found {len(accounts)} accounts:")
        
        for i, account in enumerate(accounts):
            balance = w3.eth.get_balance(account)
            balance_eth = w3.fromWei(balance, 'ether')
            print(f"Account {i}: {account}")
            print(f"  - Balance: {balance_eth} ETH")
            
            # Get transaction count
            tx_count = w3.eth.get_transaction_count(account)
            print(f"  - Transaction count: {tx_count}")
            print()
        
        print("Check complete!")
    except Exception as e:
        print(f"Error checking Ganache accounts: {e}")

if __name__ == "__main__":
    check_ganache_accounts()