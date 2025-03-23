import json
import os
import solcx

# Install specific solc version
solcx.install_solc('0.8.0')

def compile_contract():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    
    # Contract source file
    contract_file = os.path.join(project_dir, 'contracts', 'VotingContract.sol')
    
    # Output directory for compiled contract
    build_dir = os.path.join(project_dir, 'build', 'contracts')
    os.makedirs(build_dir, exist_ok=True)
    
    # Read the contract source code
    with open(contract_file, 'r') as file:
        contract_source = file.read()
    
    # Compile the contract
    compiled_sol = solcx.compile_standard({
        "language": "Solidity",
        "sources": {
            "VotingContract.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    }, solc_version='0.8.0')
    
    # Save the compiled contract
    with open(os.path.join(build_dir, 'VotingContract.json'), 'w') as file:
        json.dump(compiled_sol, file, indent=2)
    
    print(f"Contract compiled successfully. Output saved to {os.path.join(build_dir, 'VotingContract.json')}")
    
    return compiled_sol

if __name__ == "__main__":
    compile_contract()

