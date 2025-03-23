// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingContract {
    struct Candidate {
        uint256 id;
        string name;
        string area;
        uint256 voteCount;
        bool exists;
    }

    struct Voter {
        bool isRegistered;
        bool hasVoted;
        uint256 votedCandidateId;
    }

    address public admin;
    uint256 public candidatesCount;
    
    mapping(uint256 => Candidate) public candidates;
    mapping(address => Voter) public voters;
    mapping(string => bool) public voterIdRegistered;
    mapping(string => address) public voterIdToAddress;

    event CandidateRegistered(uint256 id, string name, string area);
    event VoterRegistered(address voter, string voterId);
    event VoteCast(address voter, uint256 candidateId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    modifier onlyRegisteredVoter() {
        require(voters[msg.sender].isRegistered, "Voter is not registered");
        _;
    }

    constructor() {
        admin = msg.sender;
        candidatesCount = 0;
    }

    function registerCandidate(string memory _name, string memory _area) public onlyAdmin {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(
            candidatesCount,
            _name,
            _area,
            0,
            true
        );
        
        emit CandidateRegistered(candidatesCount, _name, _area);
    }

    function registerVoter(address _voter, string memory _voterId) public onlyAdmin {
        require(!voters[_voter].isRegistered, "Voter already registered");
        require(!voterIdRegistered[_voterId], "Voter ID already registered");
        
        voters[_voter].isRegistered = true;
        voters[_voter].hasVoted = false;
        voterIdRegistered[_voterId] = true;
        voterIdToAddress[_voterId] = _voter;
        
        emit VoterRegistered(_voter, _voterId);
    }

    function vote(uint256 _candidateId) public onlyRegisteredVoter {
        require(!voters[msg.sender].hasVoted, "Voter has already voted");
        require(candidates[_candidateId].exists, "Candidate does not exist");
        
        voters[msg.sender].hasVoted = true;
        voters[msg.sender].votedCandidateId = _candidateId;
        
        candidates[_candidateId].voteCount++;
        
        emit VoteCast(msg.sender, _candidateId);
    }

    function getCandidate(uint256 _candidateId) public view returns (
        uint256 id,
        string memory name,
        string memory area,
        uint256 voteCount
    ) {
        require(candidates[_candidateId].exists, "Candidate does not exist");
        Candidate memory candidate = candidates[_candidateId];
        return (
            candidate.id,
            candidate.name,
            candidate.area,
            candidate.voteCount
        );
    }

    function getCandidatesByArea(string memory _area) public view returns (uint256[] memory) {
        uint256[] memory result = new uint256[](candidatesCount);
        uint256 count = 0;
        
        for (uint256 i = 1; i <= candidatesCount; i++) {
            if (keccak256(bytes(candidates[i].area)) == keccak256(bytes(_area))) {
                result[count] = i;
                count++;
            }
        }
        
        // Resize the array to the actual count
        uint256[] memory resized = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            resized[i] = result[i];
        }
        
        return resized;
    }

    function getVoteCount(uint256 _candidateId) public view returns (uint256) {
        require(candidates[_candidateId].exists, "Candidate does not exist");
        return candidates[_candidateId].voteCount;
    }

    function hasVoted(address _voter) public view returns (bool) {
        return voters[_voter].hasVoted;
    }

    function isRegisteredVoter(address _voter) public view returns (bool) {
        return voters[_voter].isRegistered;
    }

    function validateVoterId(string memory _voterId, address _address) public view returns (bool) {
        return voterIdToAddress[_voterId] == _address;
    }
}

