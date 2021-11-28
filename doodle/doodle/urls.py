"""doodle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lobby/public/', views.main_view_0, name='main0'),
    path('lobby/private/', views.main_view_1, name='main1'),
    path('delete/<str:room_id>/', views.delete, name='delete'),
    path('lobby/<str:room_id>/', views.main_view_2, name='main2'),
    path('menu/', views.menu, name='menu'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('register/', views.register, name='register'),
    path('', views.home , name='home'),
    path('store_msg/', views.store_msg, name='storeMsg'),
    path('kick_vote/', views.kick_vote, name='kickVote'),
    path('store_canvas/', views.store_canvas, name='storeCanvas'),
    path('start_game/', views.start_game, name='startGame'),
    path('leave_room/', views.leave_room, name='leaveRoom'),
    path('update_player/', views.update_player, name='updatePlayer'),
    path('get_data/', views.get_data, name='getData'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
