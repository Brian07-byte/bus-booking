from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('buses/', views.buses, name='buses'),
    path('blog/', views.blog, name='blog'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('booking/<int:bus_id>/', views.booking, name='booking'),
    path('schedule/<int:bus_id>/', views.schedule, name='schedule'),
    path('confirmation/<int:booking_id>/', views.confirmation, name='confirmation'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('success/<int:booking_id>/', views.success, name='success'),

]
