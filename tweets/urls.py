from django.conf.urls import url,include
from .views import Home, StreamTweets

urlpatterns = [
    url(r'^$',StreamTweets.as_view(),name='streamtweets'),
]