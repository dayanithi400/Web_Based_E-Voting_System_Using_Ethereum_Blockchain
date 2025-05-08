import os
import shutil
import json
import sys

def find_and_copy_contract_data():
    print("Finding and copying contract_data.json...")
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Project root: {project_root}")
    
    # Search for contract_data.json in the project
    contract_data_file = None
    for root, dirs, files in os.walk(project_root):
        if 'contract_data.json' in files:
            contract_data_file = os.path.join(root, 'contract_data.json')
            break
    
    if not contract_data_file:
        print("Could not find contract_data.json file in the project.")
        print("Let's create a new one.")
        
        # Create contracts directory if it doesn't exist
        contracts_dir = os.path.join(project_root, 'contracts')
        os.makedirs(contracts_dir, exist_ok=True)
        
        # Create a new contract_data.json file
        contract_data = {
            "address": input("Please enter the contract address: "),
            "abi": []  # Empty ABI for now
        }
        
        contract_data_file = os.path.join(contracts_dir, 'contract_data.json')
        with open(contract_data_file, 'w') as file:
            json.dump(contract_data, file, indent=2)
        
        print(f"Created new contract_data.json at: {contract_data_file}")
        return
    
    print(f"Found contract_data.json at: {contract_data_file}")
    
    # Create target directories
    target_dirs = [
        os.path.join(project_root, 'contracts'),
        os.path.join(project_root, 'VotingProject', 'contracts'),
        os.path.join(project_root, 'utils'),
        os.path.join(project_root, 'VotingProject', 'utils')
    ]
    
    for target_dir in target_dirs:
        os.makedirs(target_dir, exist_ok=True)
        target_file = os.path.join(target_dir, 'contract_data.json')
        
        # Copy the file
        shutil.copy2(contract_data_file, target_file)
        print(f"Copied contract_data.json to: {target_file}")
    
    print("Contract data file has been copied to multiple locations.")
    print("Please run your script again.")

if __name__ == "__main__":
    find_and_copy_contract_data()