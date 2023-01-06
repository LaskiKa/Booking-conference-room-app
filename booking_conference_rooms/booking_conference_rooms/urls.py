"""booking_conference_rooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from booking.views import main, add_new_room, delete, modify, reserve, room_details


urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/', main.as_view()),
    path('room/new/', add_new_room.as_view()),
    re_path('room/(?P<id>(\d)+)/', room_details.as_view()),
    re_path('room/delete/(?P<id>(\d)+)/', delete.as_view()),
    re_path('room/modify/(?P<id>(\d)+)/', modify.as_view()),
    re_path('room/reserve/(?P<id>(\d)+)/', reserve.as_view()),

]
