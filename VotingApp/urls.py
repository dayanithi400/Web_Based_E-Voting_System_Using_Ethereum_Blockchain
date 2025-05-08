from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.voting_dashboard, name='voting_dashboard'),
    path('cast-vote/', views.cast_vote, name='cast_vote'),
    path('get_overall_results/', views.get_overall_results, name='get_overall_results'),
    path('get_constituencies/', views.get_constituencies, name='get_constituencies'),
    path('candidate-registration/', views.candidate_registration, name='candidate_registration'),
    path('get-results/', views.get_results, name='get_results'),
    path('profile/', views.profile_view, name='profile'), 
    path('results/', views.results_view, name='results'),
    path('voter_count/', views.get_voter_count, name='get_voter_count'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
