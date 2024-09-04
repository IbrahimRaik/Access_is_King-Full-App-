from django.urls import path
from Chat import views

urlpatterns = [
    path('start/', views.start_convo, name='start_convo'),
    path('<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('all_conversatons', views.conversations, name='conversations'),
    path('messages/',views.postMessage, name="messages"),

    path('group/create/', views.create_group, name='create_group'),
    path('groups-list/', views.list_groups, name='list_groups'),
    path('group/<int:group_id>/add-member/', views.add_group_member, name='add_group_member'),
    path('group/<int:group_id>/send-message/', views.send_group_message, name='send_group_message'),
    path('group/<int:group_id>/messages/', views.get_group_messages, name='get_group_messages'),

    # Event URLs
    path('event/create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/join/', views.join_event, name='join_event'),
    path('event/<int:event_id>/participants/', views.get_event_participants, name='get_event_participants'),
]