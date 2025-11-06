from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # dashboard as root
    path('dashboard/', views.dashboard, name='dashboard'),

    # rooms management
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/delete/<int:pk>/', views.room_delete, name='room_delete'),

    # checkin / checkout
    path('checkin/', views.checkin_view, name='checkin'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('bill/<int:booking_id>/', views.bill_view, name='bill'),
]
