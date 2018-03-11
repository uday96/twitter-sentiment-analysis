import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from django.conf import settings
import json, random
from sentiment_analysis import sentiment_score

consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_SECRET

def searchTwitter(query):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    search_results = api.search(q=query, count=100)
    return [status._json for status in search_results]

def createHTML(tweet):
    contentString = '<div class="infowindow-content"><blockquote class="twitter-tweet" lang="en"><p>'
    contentString = contentString + tweet["text"]+'</p>&mdash; '
    contentString = contentString + tweet["user"]["name"] +' (@'+tweet["user"]["screen_name"]+')'
    contentString = contentString + ' <a href="https://twitter.com/'+tweet["user"]["screen_name"]+'/statuses/'+tweet["id_str"]+'">'
    contentString = contentString + '</a></blockquote></div>'
    print "\n"+contentString+"\n"
    return contentString

def locs(region):
    region_map = {
        "united states": [-120.001,55.9493,-89.9326,32.5904],
    }
    lng = random.uniform(region_map[region][0],region_map[region][2])
    lat = random.uniform(region_map[region][1],region_map[region][3])
    return lat,lng

data_list = []
curr_region = "united states"
count = 0

class listener(StreamListener):

    def on_data(self, data):
        global count
        global data_list
        #How many tweets you want to find, could change to time based
        # if count <= 2000:
        #     json_data = json.loads(data)
        #     coords = json_data["coordinates"]
        #     if coords is not None:
        #        print coords["coordinates"]
        #        lon = coords["coordinates"][0]
        #        lat = coords["coordinates"][1]
        #        data_list.append(json_data)
        #        print json_data,"\n"
        #        count += 1
        #     return True
        # else:
        #     return False
        if count < 50:
            json_data = json.loads(data)
            lat,lng = locs(curr_region)
            data_list.append({
                "htmlStr": createHTML(json_data),
                "confidence": sentiment_score(json_data["text"]),
                "lat": lat,
                "lng": lng,
            })
            count += 1
            return True
        else:
            return False

    def on_error(self, status):
        print status

def streamTwitter(query,region):
    global count
    global curr_region
    count = 0
    curr_region = region
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterStream = Stream(auth, listener())
    #What you want to search for here
    # twitterStream.filter(locations=[76.838069,28.412593,77.348458,28.881338])
    twitterStream.filter(track=[query],async=True)