from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='payments_index'),
    path('start/', views.start_payment, name='start_payment'),
]