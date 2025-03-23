from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Candidate, Vote
from VotingProject.utils.web3_utils import Web3Utils
import json
import traceback

# Initialize Web3 utilities
# try:
#     web3_utils = Web3Utils()
# except Exception as e:
#     web3_utils = None
#     print(f"Error initializing Web3Utils: {e}")
try:
    web3_utils = Web3Utils()
    print("Web3Utils initialized successfully")
except Exception as e:
    web3_utils = None
    print(f"Error initializing Web3Utils: {e}")
    traceback.print_exc()

# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         voter_id = request.POST.get('voter_id')
#         area = request.POST.get('area')
        
#         # Check if user already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists')
#             return render(request, 'registration.html')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email already exists')
#             return render(request, 'registration.html')
        
#         if User.objects.filter(voter_id=voter_id).exists():
#             messages.error(request, 'Voter ID already exists')
#             return render(request, 'registration.html')
        
#         # Create a new Ethereum account for the user
#         if web3_utils:
#             eth_address, _ = web3_utils.get_new_account()
#         else:
#             eth_address = None
#             messages.warning(request, 'Blockchain connection not available. Some features may be limited.')
        
#         # Create user
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             voter_id=voter_id,
#             area=area,
#             eth_address=eth_address
#         )
        
#         # Register voter on blockchain
#         if web3_utils and eth_address:
#             try:
#                 web3_utils.register_voter(eth_address, voter_id)
#                 user.is_registered_on_blockchain = True
#                 user.save()
#             except Exception as e:
#                 messages.warning(request, f'User created but blockchain registration failed: {e}')
        
#         messages.success(request, 'Registration successful. Please log in.')
#         return redirect('login')
    
#     return render(request, 'registration.html')
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        voter_id = request.POST.get('voter_id')
        area = request.POST.get('area')
        
        # New fields
        aadhar_number = request.POST.get('aadhar_number')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        ward_number = request.POST.get('ward_number')
        taluk = request.POST.get('taluk')
        district = request.POST.get('district')
        pin_code = request.POST.get('pin_code')
        state = request.POST.get('state')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'registration.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'registration.html')
        
        if User.objects.filter(voter_id=voter_id).exists():
            messages.error(request, 'Voter ID already exists')
            return render(request, 'registration.html')
        
        if aadhar_number and User.objects.filter(aadhar_number=aadhar_number).exists():
            messages.error(request, 'Aadhar number already exists')
            return render(request, 'registration.html')
        
        # Create a new Ethereum account for the user
        if web3_utils:
            eth_address, _ = web3_utils.get_new_account()
        else:
            eth_address = None
            messages.warning(request, 'Blockchain connection not available. Some features may be limited.')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            voter_id=voter_id,
            area=area,
            eth_address=eth_address,
            aadhar_number=aadhar_number,
            phone_number=phone_number,
            date_of_birth=date_of_birth if date_of_birth else None,
            ward_number=ward_number,
            taluk=taluk,
            district=district,
            pin_code=pin_code,
            state=state
        )
        
        # Register voter on blockchain
        if web3_utils and eth_address:
            try:
                web3_utils.register_voter(eth_address, voter_id)
                user.is_registered_on_blockchain = True
                user.save()
            except Exception as e:
                messages.warning(request, f'User created but blockchain registration failed: {e}')
        
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')
    
    return render(request, 'registration.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'profile.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        voter_id = request.POST.get('voter_id')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Verify voter ID
            if user.voter_id != voter_id:
                messages.error(request, 'Invalid Voter ID')
                return render(request, 'login.html')
            
            login(request, user)
            return redirect('voting_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def voting_dashboard(request):
    user = request.user
    
    # Get candidates in user's area
    if web3_utils:
        try:
            # First check if the contract is accessible
            try:
                candidates_count = web3_utils.contract.functions.candidatesCount().call()
                print(f"Found {candidates_count} candidates in total")
            except Exception as e:
                print(f"Error accessing contract: {e}")
                messages.error(request, f'Error accessing blockchain: {e}')
                return render(request, 'voting_dashboard.html', {
                    'error': 'Could not transact with/call contract function, is contract deployed correctly and chain synced?',
                    'user_area': user.area
                })
            
            # Get candidates by area
            candidate_ids = web3_utils.get_candidates_by_area(user.area)
            print(f"Found {len(candidate_ids)} candidates in area {user.area}")
            
            candidates = []
            
            for candidate_id in candidate_ids:
                candidate_data = web3_utils.get_candidate(candidate_id)
                candidates.append({
                    'id': candidate_data[0],
                    'name': candidate_data[1],
                    'area': candidate_data[2],
                    'vote_count': candidate_data[3]
                })
            
            # Check if user has already voted
            has_voted = web3_utils.has_voted(user.eth_address)
            
            context = {
                'candidates': candidates,
                'has_voted': has_voted,
                'user_area': user.area
            }
            
            return render(request, 'voting_dashboard.html', context)
        except Exception as e:
            print(f"Error in voting_dashboard: {e}")
            traceback.print_exc()
            messages.error(request, f'Error fetching candidates: {e}')
            return render(request, 'voting_dashboard.html', {
                'error': str(e),
                'user_area': user.area
            })
    else:
        messages.error(request, 'Blockchain connection not available')
        return render(request, 'voting_dashboard.html', {
            'error': 'Blockchain connection not available',
            'user_area': user.area
        })
    
    
@login_required
def cast_vote(request):
    if request.method == 'POST':
        candidate_id = int(request.POST.get('candidate_id'))
        user = request.user
        
        if web3_utils:
            try:
                # Check if user has already voted
                if web3_utils.has_voted(user.eth_address):
                    return JsonResponse({'success': False, 'message': 'You have already voted'})
                
                # Cast vote on blockchain
                tx_receipt = web3_utils.vote(user.eth_address, candidate_id)
                
                # Save vote in database
                candidate = Candidate.objects.get(blockchain_id=candidate_id)
                Vote.objects.create(
                    voter=user,
                    candidate=candidate,
                    transaction_hash=tx_receipt.transactionHash.hex()
                )
                
                return JsonResponse({'success': True, 'message': 'Vote cast successfully'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error casting vote: {e}'})
        else:
            return JsonResponse({'success': False, 'message': 'Blockchain connection not available'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# @login_required
# def candidate_registration(request):
#     if not request.user.is_staff:
#         messages.error(request, 'You do not have permission to register candidates')
#         return redirect('voting_dashboard')
    
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         area = request.POST.get('area')
        
#         if web3_utils:
#             try:
#                 # Register candidate on blockchain
#                 tx_receipt = web3_utils.register_candidate(name, area)
                
#                 # Get candidate ID from event logs
#                 logs = web3_utils.contract.events.CandidateRegistered().process_receipt(tx_receipt)
#                 candidate_id = logs[0]['args']['id']
                
#                 # Save candidate in database
#                 Candidate.objects.create(
#                     name=name,
#                     area=area,
#                     blockchain_id=candidate_id
#                 )
                
#                 messages.success(request, 'Candidate registered successfully')
#                 return redirect('candidate_registration')
#             except Exception as e:
#                 messages.error(request, f'Error registering candidate: {e}')
#         else:
#             messages.error(request, 'Blockchain connection not available')
    
#     # Get all candidates
#     candidates = Candidate.objects.all()
    
#     return render(request, 'candidate_registration.html', {'candidates': candidates})
# @login_required
# def candidate_registration(request):
#     if not request.user.is_staff:
#         messages.error(request, 'You do not have permission to register candidates')
#         return redirect('voting_dashboard')
    
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         area = request.POST.get('area')
        
#         if web3_utils:
#             try:
#                 # Register candidate on blockchain
#                 tx_receipt = web3_utils.register_candidate(name, area)
                
#                 # Get candidate ID from event logs - THIS IS THE PART THAT NEEDS FIXING
#                 # REPLACE THE FOLLOWING LINE:
#                 # logs = web3_utils.contract.events.CandidateRegistered().process_receipt(tx_receipt)
#                 # WITH THESE LINES:
                
#                 # Get the latest candidate ID
#                 candidate_id = web3_utils.contract.functions.candidatesCount().call()
                
#                 # Save candidate in database
#                 Candidate.objects.create(
#                     name=name,
#                     area=area,
#                     blockchain_id=candidate_id
#                 )
                
#                 messages.success(request, 'Candidate registered successfully')
#                 return redirect('candidate_registration')
#             except Exception as e:
#                 messages.error(request, f'Error registering candidate: {e}')
#         else:
#             messages.error(request, 'Blockchain connection not available')
    
#     # Get all candidates
#     candidates = Candidate.objects.all()
    
#     return render(request, 'candidate_registration.html', {'candidates': candidates})
# def get_results(request):
#     if web3_utils:
#         try:
#             # Get all candidates from database
#             candidates = Candidate.objects.all()
#             results = []
            
#             for candidate in candidates:
#                 vote_count = web3_utils.get_vote_count(candidate.blockchain_id)
#                 results.append({
#                     'id': candidate.blockchain_id,
#                     'name': candidate.name,
#                     'area': candidate.area,
#                     'vote_count': vote_count
#                 })
            
#             return JsonResponse({'success': True, 'results': results})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': f'Error fetching results: {e}'})
#     else:
#         return JsonResponse({'success': False, 'message': 'Blockchain connection not available'})

# def get_results(request):
#     if web3_utils:
#         try:
#             # Get all candidates from database
#             candidates = Candidate.objects.all()
#             results = []
            
#             for candidate in candidates:
#                 try:
#                     # First check if the candidate exists on the blockchain
#                     try:
#                         # Try to get the candidate details first to verify it exists
#                         web3_utils.get_candidate(candidate.blockchain_id)
#                         # If we get here, the candidate exists, so get the vote count
#                         vote_count = web3_utils.get_vote_count(candidate.blockchain_id)
#                     except Exception as e:
#                         # Candidate doesn't exist on blockchain, set vote count to 0
#                         print(f"Candidate {candidate.name} (ID: {candidate.blockchain_id}) doesn't exist on blockchain: {e}")
#                         vote_count = 0
                    
#                     results.append({
#                         'id': candidate.blockchain_id,
#                         'name': candidate.name,
#                         'area': candidate.area,
#                         'vote_count': vote_count
#                     })
#                 except Exception as e:
#                     print(f"Error getting vote count for candidate {candidate.name}: {e}")
            
#             return JsonResponse({'success': True, 'results': results})
#         except Exception as e:
#             print(f"Error in get_results: {e}")
#             return JsonResponse({'success': False, 'message': f'Error fetching results: {e}'})
#     else:
#         return JsonResponse({'success': False, 'message': 'Blockchain connection not available'})

def candidate_registration(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'You do not have permission to register candidates')
        return redirect('voting_dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        area = request.POST.get('area')
        party = request.POST.get('party')
        party_leader = request.POST.get('party_leader')
        picture = request.FILES.get('picture')
        
        if not name or not area:
            messages.error(request, 'Name and area are required')
            return render(request, 'candidate_registration.html')
        
        # Get the next available blockchain ID
        next_id = 1
        if Candidate.objects.exists():
            next_id = Candidate.objects.aggregate(models.Max('blockchain_id'))['blockchain_id__max'] + 1
        
        # Register candidate on blockchain
        if web3_utils:
            try:
                tx_receipt = web3_utils.register_candidate(name, area, next_id)
                
                # Create candidate in database
                candidate = Candidate.objects.create(
                    name=name,
                    area=area,
                    blockchain_id=next_id,
                    party=party,
                    party_leader=party_leader,
                    picture=picture
                )
                
                messages.success(request, f'Candidate {name} registered successfully with ID {next_id}')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error registering candidate on blockchain: {e}')
        else:
            messages.error(request, 'Blockchain connection not available')
    
    return render(request, 'candidate_registration.html')

def get_results(request):
    try:
        if not web3_utils:
            return JsonResponse({'success': False, 'message': 'Blockchain connection not available'})
        
        # Get all candidates
        candidates = Candidate.objects.all()
        results = []
        
        for candidate in candidates:
            try:
                # Get vote count from blockchain
                vote_count = web3_utils.get_vote_count(candidate.blockchain_id)
                
                # Add to results
                results.append({
                    'name': candidate.name,
                    'area': candidate.area,
                    'vote_count': vote_count,
                    'party': candidate.party if candidate.party else 'Independent'
                })
            except Exception as e:
                print(f"Error getting vote count for candidate {candidate.name}: {e}")
        
        # Sort by vote count (descending)
        results = sorted(results, key=lambda x: x['vote_count'], reverse=True)
        
        return JsonResponse({'success': True, 'results': results})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

