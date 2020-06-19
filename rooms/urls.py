from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('rooms/student_banned/', views.banned_viewers,name='viewer_banned'),
    path('rooms/forms/<room>/<uuid>/', views.auth_join, name='auth_join'),
    path('rooms/<str:room_name>/', views.show_chat_page, name='room_detail'),
    path('rooms/', views.RoomView.as_view(),name='rooms'),
    path('create_room/', views.create_room,name='create_room'),
    path('<username>/rooms/', views.CreatorCreatedRooms.as_view(), name='teacher_created_rooms'),
    path('rooms/<uuid>/join/', views.join_room,name='join_room'),
    path('rooms/<uuid>/leave/', views.leave_room,name='leave_room'),
    path('rooms/ban_student/<uuid>/<user_id>/', views.ban_viewer, name='ban_student'),
]



