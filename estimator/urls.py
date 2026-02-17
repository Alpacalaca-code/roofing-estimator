from django.urls import path
from . import views

urlpatterns = [
    # This makes the estimator the very first thing you see (the home page)
    path('', views.calculate_view, name='estimator_home'),
    
    # You can add more paths here later, like:
    # path('dashboard/', views.dashboard, name='dashboard'),
]