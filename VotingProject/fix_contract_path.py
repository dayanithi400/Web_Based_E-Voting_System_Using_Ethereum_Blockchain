import os
import sys

def fix_contract_path():
    print("Fixing contract data path in Web3Utils class...")
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Project root: {project_root}")
    
    # Find the web3_utils.py file
    web3_utils_path = os.path.join(project_root, 'VotingProject', 'utils', 'web3_utils.py')
    if not os.path.exists(web3_utils_path):
        web3_utils_path = os.path.join(project_root, 'utils', 'web3_utils.py')
    
    if not os.path.exists(web3_utils_path):
        print("Could not find web3_utils.py file. Please provide the correct path.")
        return
    
    print(f"Found web3_utils.py at: {web3_utils_path}")
    
    # Find the contract_data.json file
    contract_data_paths = [
        os.path.join(project_root, 'contracts', 'contract_data.json'),
        os.path.join(project_root, 'VotingProject', 'contracts', 'contract_data.json'),
        os.path.join(project_root, 'utils', 'contract_data.json'),
        os.path.join(project_root, 'VotingProject', 'utils', 'contract_data.json')
    ]
    
    contract_data_path = None
    for path in contract_data_paths:
        if os.path.exists(path):
            contract_data_path = path
            break
    
    if not contract_data_path:
        print("Could not find contract_data.json file. Please provide the correct path.")
        return
    
    print(f"Found contract_data.json at: {contract_data_path}")
    
    # Read the web3_utils.py file
    with open(web3_utils_path, 'r') as file:
        content = file.read()
    
    # Update the contract_path line
    import re
    updated_content = re.sub(
        r'contract_path = os\.path\.join$$.*?$$',
        f"contract_path = '{contract_data_path.replace('\\', '\\\\')}'",
        content
    )
    
    # Write the updated content back to the file
    with open(web3_utils_path, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated contract_path in {web3_utils_path}")
    print("Please run your script again.")

if __name__ == "__main__":
    fix_contract_path()