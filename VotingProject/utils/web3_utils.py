import json
import os
from web3 import Web3

class Web3Utils:
    def __init__(self):
        # Connect to Ganache
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        
        # Check if connected
        if not self.w3.isConnected():
            raise Exception("Failed to connect to Ethereum node.")
        
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(current_dir)
        
        # Load contract info
        contract_info_path = os.path.join(project_dir, 'deployment', 'contract_info.json')
        
        try:
            with open(contract_info_path, 'r') as file:
                contract_info = json.load(file)
                
            self.contract_address = contract_info['contract_address']
            self.abi = contract_info['abi']
            self.admin_account = contract_info['deployer_account']
            
            # Create contract instance
            self.contract = self.w3.eth.contract(
                address=self.contract_address,
                abi=self.abi
            )
        except FileNotFoundError:
            raise Exception("Contract info not found. Please deploy the contract first.")
    
    def register_candidate(self, name, area):
        """Register a new candidate"""
        tx_hash = self.contract.functions.registerCandidate(name, area).transact({
            'from': self.admin_account
        })
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def register_voter(self, voter_address, voter_id):
        """Register a new voter"""
        tx_hash = self.contract.functions.registerVoter(voter_address, voter_id).transact({
            'from': self.admin_account
        })
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def vote(self, voter_address, candidate_id):
        """Cast a vote for a candidate"""
        tx_hash = self.contract.functions.vote(candidate_id).transact({
            'from': voter_address
        })
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    
    def get_candidate(self, candidate_id):
        """Get candidate details"""
        return self.contract.functions.getCandidate(candidate_id).call()
    
    def get_candidates_by_area(self, area):
        """Get candidates by area"""
        return self.contract.functions.getCandidatesByArea(area).call()
    
    def get_vote_count(self, candidate_id):
        """Get vote count for a candidate"""
        return self.contract.functions.getVoteCount(candidate_id).call()
    
    def has_voted(self, voter_address):
        """Check if a voter has already voted"""
        return self.contract.functions.hasVoted(voter_address).call()
    
    def is_registered_voter(self, voter_address):
        """Check if an address is registered as a voter"""
        return self.contract.functions.isRegisteredVoter(voter_address).call()
    
    def validate_voter_id(self, voter_id, address):
        """Validate if voter ID matches the address"""
        return self.contract.functions.validateVoterId(voter_id, address).call()
    
    def get_new_account(self):
        """Create a new Ethereum account"""
        account = self.w3.eth.account.create()
        return account.address, account.key.hex()

