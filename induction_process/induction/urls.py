from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('applicant_dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('create_applicant_profile/', views.create_applicant_profile, name='create_applicant_profile'),
]
