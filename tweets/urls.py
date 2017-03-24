from django.conf.urls import url,include
from .views import Home, StreamTweets,VisualiseTweets

urlpatterns = [
    url(r'^$',StreamTweets.as_view(),name='streamtweets'),
    url(r'^visualise/',VisualiseTweets.as_view(),name='visualisetweets'),
]