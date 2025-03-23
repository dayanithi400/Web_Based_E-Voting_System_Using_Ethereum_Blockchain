import os
import sys
import json

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(os.path.dirname(project_dir))

from VotingProject.utils.compile_contract import compile_contract
from VotingProject.utils.deploy_contract import deploy_contract

def main():
    print("Compiling VotingContract...")
    compile_contract()
    
    print("\nDeploying VotingContract...")
    contract_address, abi = deploy_contract()
    
    print("\nDeployment Summary:")
    print(f"Contract Address: {contract_address}")
    print("Contract ABI saved to deployment/contract_info.json")
    
    print("\nNext Steps:")
    print("1. Make sure your Django settings are configured to use the deployed contract")
    print("2. Run the Django server: python manage.py runserver")
    print("3. Connect MetaMask to Ganache (http://127.0.0.1:7545, Chain ID: 1337)")
    print("4. Import Ganache accounts into MetaMask for testing")

if __name__ == "__main__":
    main()

