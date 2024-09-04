from django.urls import path
from AccessIsKing.views import CityView , NewCommentsView  ,NewMessagesView

urlpatterns = [
    path('city', CityView.as_view(), name='citynames'),
    path('new-comments', NewCommentsView.as_view(), name='citynames'),
    path('new-messages', NewMessagesView.as_view(), name='citynames'),
]
