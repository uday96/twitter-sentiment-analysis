from django.conf.urls import url,include
from .views import Home, StreamTweets,MapsInterface

urlpatterns = [
    url(r'^$',StreamTweets.as_view(),name='streamtweets'),
    url(r'^maps/',MapsInterface.as_view(),name='maps'),
]