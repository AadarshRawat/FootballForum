from django.urls import path
from . import views

urlpatterns = [
    path('login',views.LoginPage,name='login'),
    path('register',views.registerPage,name='register'),
    path('logout',views.LogoutPage,name='logout'),
    path('',views.Home,name='home'),
    path('Roomfunc/<int:pk>/',views.Rooms,name='room'),
    path('profile/<int:pk>/',views.userProfile,name='profile'),
    path('create-room',views.createRoom,name='create-room'),
    path('update-room/<int:pk>',views.updateRoom,name='update-room'),
    path('delete-room/<int:pk>',views.deleteRoom,name='delete-room'),
    path('delete-message/<int:pk>',views.deleteMessage,name='delete-message'),
    path('profile/<int:pk>',views.userProfile,name='profile'),
    path('update-user',views.updateUser,name='update-user'),
    path('activity/', views.activityPage, name="activity"),
    path('topics/', views.topicsPage, name="topics"),
    path('update-message/<int:pk>', views.updateMessage, name="update-message"),


]
