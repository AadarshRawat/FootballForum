from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='home'),
    path('Roomfunc/<int:pk>/',views.Rooms,name='room'),
]
