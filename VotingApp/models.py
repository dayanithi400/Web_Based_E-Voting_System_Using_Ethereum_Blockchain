from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    voter_id = models.CharField(max_length=50, unique=True)
    eth_address = models.CharField(max_length=42, unique=True, null=True, blank=True)
    area = models.CharField(max_length=100)
    is_registered_on_blockchain = models.BooleanField(default=False)
    
    # New fields
    aadhar_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    ward_number = models.CharField(max_length=20, null=True, blank=True)
    taluk = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.voter_id})"

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    blockchain_id = models.IntegerField(unique=True)
    
    # New fields
    picture = models.ImageField(upload_to='candidate_pictures/', null=True, blank=True)
    party = models.CharField(max_length=100, null=True, blank=True)
    party_leader = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.area} (ID: {self.blockchain_id})"

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=66)
    
    class Meta:
        unique_together = ('voter',)
    
    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name}"
