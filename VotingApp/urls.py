from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.voting_dashboard, name='voting_dashboard'),
    path('cast-vote/', views.cast_vote, name='cast_vote'),
    path('candidate-registration/', views.candidate_registration, name='candidate_registration'),
    path('get-results/', views.get_results, name='get_results'),
    path('profile/', views.profile_view, name='profile'), 
]
