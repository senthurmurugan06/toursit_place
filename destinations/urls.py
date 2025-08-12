from django.urls import path
from . import views
# Remove: from allauth.account.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('place/<int:pk>/', views.place_detail, name='place_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/chat/history/', views.get_chat_history, name='get_chat_history'),
    path('accounts/logout/', views.custom_logout, name='account_logout'),
] 