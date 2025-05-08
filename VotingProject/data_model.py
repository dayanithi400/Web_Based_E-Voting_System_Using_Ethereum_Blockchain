import os
import django
import sys
import random
from datetime import datetime, timedelta

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')
django.setup()

from VotingApp.models import User
from django.utils.crypto import get_random_string

def generate_voter_id():
    prefix = "TN"
    digits = ''.join(random.choices('0123456789', k=8))
    return f"{prefix}{digits}"

def generate_aadhar_number():
    return ''.join(random.choices('0123456789', k=12))

def generate_phone_number():
    return f"91{''.join(random.choices('0123456789', k=10))}"

def generate_random_date(start_year=1960, end_year=2002):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_days = random.randrange((end_date - start_date).days)
    return start_date + timedelta(days=random_days)

def create_tamil_nadu_voters(num_voters=10):
    district_data = {
        'taluk': 'Tiruvannamalai',
        'district': 'Tiruvannamalai',
        'pin_code': '606752',
        'state': 'Tamil Nadu',
        'area': 'Kilpennathur'
    }

    ward_numbers = [f"Ward {i}" for i in range(1, 11)]

    mock_usernames = [
        "Arun Kumar", "Divya Rani", "Rajesh P", "Sneha S", "Vignesh M",
        "Rekha D", "Mani K", "Meena J", "Karthik S", "Latha N",
        "Naveen R", "Priya V", "Dinesh T", "Anitha K", "Sathish V",
        "Pooja M", "Gokul N", "Keerthi A", "Bala R", "Vidhya S"
    ]

    print(f"Creating {num_voters} sample voters from Tamil Nadu...")

    created_count = 0
    for i in range(num_voters):
        if i < len(mock_usernames):
            username = mock_usernames[i]
        else:
            first = get_random_string(5).capitalize()
            last = get_random_string(5).capitalize()
            username = f"{first} {last}"

        if User.objects.filter(username=username).exists():
            continue

        voter_id = generate_voter_id()
        while User.objects.filter(voter_id=voter_id).exists():
            voter_id = generate_voter_id()

        aadhar_number = generate_aadhar_number()
        while User.objects.filter(aadhar_number=aadhar_number).exists():
            aadhar_number = generate_aadhar_number()

        user = User.objects.create_user(
            username=username,
            email=f"{username.replace(' ', '').lower()}@example.com",
            password="password123",
            voter_id=voter_id,
            aadhar_number=aadhar_number,
            phone_number=generate_phone_number(),
            date_of_birth=generate_random_date(),
            ward_number=random.choice(ward_numbers),
            taluk=district_data['taluk'],
            district=district_data['district'],
            pin_code=district_data['pin_code'],
            state=district_data['state'],
            area=district_data['area']
        )

        print(f"Created user: {user.username} with voter ID: {user.voter_id}")
        created_count += 1

    print(f"{created_count} sample voters created successfully!")

if __name__ == "__main__":
    create_tamil_nadu_voters(20)
