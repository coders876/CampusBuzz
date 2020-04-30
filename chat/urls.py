from django.urls import path

from . import views
app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:sender_id>/<int:receiver_id>/', views.room, name='room'),
]