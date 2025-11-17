from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('book/<str:destination>/', views.book_trip, name='book_trip'),
    path('list/', views.booking_list, name='booking_list'),
    path('summary/', views.booking_summary, name='booking_summary'),
]
