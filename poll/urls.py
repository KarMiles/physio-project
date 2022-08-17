# Imports
# 3rd party:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.urls import path

# Internal:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from . import views as poll_views


# URL patterns for the app poll

urlpatterns = [
    path('', poll_views.poll_home, name='poll_home'),
    path('create/', poll_views.poll_create, name='poll_create'),
    path('vote/<poll_id>/', poll_views.poll_vote, name='poll_vote'),
    path('results/<poll_id>/', poll_views.poll_results, name='poll_results'),
    path('delete/<poll_id>/', poll_views.poll_delete, name='poll_delete'),
]
