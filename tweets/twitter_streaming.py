import tweepy
import threading, logging, time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from django.conf import settings
import string

consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_SECRET

mytopic='TwitterStream'# ex. 'twitterstream', or 'test' ...

######################################################################
#Create a handler for the streaming data that stays open...
######################################################################

class StdOutListener(tweepy.StreamListener):

    #Handler
    ''' Handles data received from the stream. '''

    ######################################################################
    #For each status event
    ######################################################################
    tweet_count = 0;

    def on_status(self, status):
        
        # Prints the text of the tweet
        #print '%d,%d,%d,%s,%s' % (status.user.followers_count, status.user.friends_count,status.user.statuses_count, status.user.id_str, status.user.screen_name)
        
        # Schema changed to add the tweet text
        self.tweet_count = self.tweet_count + 1
        if self.tweet_count < 10:
            #print '%d,%d,%d,%s,%s' % (status.user.followers_count, status.user.friends_count,status.user.statuses_count, status.text, status.user.screen_name)
            message =  str(status.user.followers_count) + ',' + str(status.user.friends_count) + ',' + str(status.user.statuses_count) + ',' + status.text + ',' + status.user.screen_name
            msg = filter(lambda x: x in string.printable, message)
            print "\n"+msg+"\n"
        else:
            return False
        # try:
        #     #write out to kafka topic
        #     producer.send_messages(mytopic, str(msg))
        # except Exception, e:
        #     return True
        
        return True
       
    ######################################################################
    #Supress Failure to keep demo running... In a production situation 
    #Handle with seperate handler
    ######################################################################
 
    def on_error(self, status_code):

        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):

        print('Timeout...')
        return True # To continue listening

######################################################################
#Main Loop Init
######################################################################


def streamTwitter(keywords,location):
    
    listener = StdOutListener()

    #sign oath cert

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    #uncomment to use api in stream for data send/retrieve algorythms 
    #api = tweepy.API(auth)

    stream = tweepy.Stream(auth, listener)

    ######################################################################
    #Sample delivers a stream of 1% (random selection) of all tweets
    ######################################################################
    #stream.sample()
    #client = KafkaClient("localhost:9092")
    #producer = SimpleProducer(client)

    ######################################################################
    #Custom Filter rules pull all traffic for those filters in real time.
    #Bellow are some examples add or remove as needed...
    ######################################################################
    #A Good demo stream of reasonable amount
    #stream.filter(track=['actian', 'BigData', 'Hadoop', 'Predictive', 'Quantum', 'bigdata', 'Analytics', 'IoT'])
    #Hadoop Summit following
    stream.filter(track=keywords,languages=['en'])

