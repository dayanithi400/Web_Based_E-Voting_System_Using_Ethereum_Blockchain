"""
WSGI config for VotingProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')

# application = get_wsgi_application()

# VotingProject/wsgi.py
import os
import sys

# Apply the patch before importing Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import inspect_patch  # This must be imported first

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VotingProject.settings')

application = get_wsgi_application()