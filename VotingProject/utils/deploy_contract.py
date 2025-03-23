import json
import os
from web3 import Web3

def deploy_contract():
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    
    # Check if connected
    if not w3.isConnected():
        print("Failed to connect to Ethereum node.")
        return None
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    
    # Load compiled contract
    compiled_contract_path = os.path.join(project_dir, 'build', 'contracts', 'VotingContract.json')
    
    with open(compiled_contract_path, 'r') as file:
        contract_json = json.load(file)
    
    # Get contract data
    contract_data = contract_json['contracts']['VotingContract.sol']['VotingContract']
    abi = contract_data['abi']
    bytecode = contract_data['evm']['bytecode']['object']
    
    # Get account to deploy from
    accounts = w3.eth.accounts
    deployer_account = accounts[0]
    
    # Create contract instance
    VotingContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Deploy contract
    tx_hash = VotingContract.constructor().transact({'from': deployer_account})
    
    # Wait for transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    
    print(f"Contract deployed at address: {contract_address}")
    
    # Save deployment info
    deployment_dir = os.path.join(project_dir, 'deployment')
    os.makedirs(deployment_dir, exist_ok=True)
    
    deployment_info = {
        'contract_address': contract_address,
        'deployer_account': deployer_account,
        'abi': abi
    }
    
    with open(os.path.join(deployment_dir, 'contract_info.json'), 'w') as file:
        json.dump(deployment_info, file, indent=2)
    
    return contract_address, abi

if __name__ == "__main__":
    deploy_contract()

