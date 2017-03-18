import tweepy
import threading, logging, time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from kafka import KafkaProducer
from django.conf import settings
import string, json

consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_SECRET

mytopic='test'
keywords = []


######################################################################
#Create a handler for the streaming data that stays open...
######################################################################

class StdOutListener(tweepy.StreamListener):

    #Handler
    ''' Handles data received from the stream. '''

    ######################################################################
    #For each status event
    ######################################################################

    tweet_count =0

    def on_status(self, status):
        print keywords
        self.tweet_count = self.tweet_count + 1
        if self.tweet_count < 5:
            message =  status.text
            msg = filter(lambda x: x in string.printable, message)
            print "\n"+msg+"\n"
            tweetsdump = open("tweetsdump.txt","a")
            tweetsdump.write(json.dumps(status._json, indent=4))
            tweetsdump.write("\n\n")
            tweetsdump.close()
        else:
            return False
                
        # try:
        #     #write out to kafka topic
        #     producer = KafkaProducer(bootstrap_servers='localhost:9092')
        #     future = producer.send('test', (str(json.dumps(status._json, indent=4))+"\n"))
        #     record_metadata = future.get(timeout=10)
        #     print record_metadata.topic
        #     print record_metadata.partition
        #     print record_metadata.offset
        # except Exception, e:
        #     print str(e)
        #     return True
        
        return True
       
    ######################################################################
    #Supress Failure to keep demo running... In a production situation 
    #Handle with seperate handler
    ######################################################################
 
    def on_error(self, status_code):

        print('Got an error with status code: ' + str(status_code))
        return False # To stop listening
 
    def on_timeout(self):

        print('Timeout...')
        return False # To stop listening


def streamTwitter(keywordargs,latlngs):
    
    global keywords
    keywords = keywordargs

    tweetsdump = open("tweetsdump.txt","w")
    tweetsdump.close()

    listener = StdOutListener()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, listener)

    stream.filter(locations=latlngs)
    