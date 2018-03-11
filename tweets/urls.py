from django.conf.urls import url,include
from .views import Home, StreamTweets,ProduceTweets,ConsumeTweets

urlpatterns = [
    url(r'^$',StreamTweets.as_view(),name='streamtweets'),
    url(r'^produce/',ProduceTweets.as_view(),name='producetweets'),
    url(r'^consume/',ConsumeTweets.as_view(),name='consumetweets'),
]