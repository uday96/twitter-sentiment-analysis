import tweepy
import threading, logging, time
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer
from kafka import KafkaProducer
from django.conf import settings
import string, json
from django.shortcuts import render, redirect

consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_SECRET

mytopic=""
keywords = []
streams = []

######################################################################
#Create a handler for the streaming data that stays open...
######################################################################

class StdOutListener(tweepy.StreamListener):

    #Handler
    ''' Handles data received from the stream. '''

    ######################################################################
    #For each status event
    ######################################################################
    tweet_flag =0
    tweet_count =0

    def on_status(self, status):
        print keywords
        if self.tweet_count < 100:
            message =  status.text
            for i in range(len(keywords)):
                if keywords[i].lower() in message.lower():
                    self.tweet_flag = 1
                    break
                entity_field = status.entities
                if entity_field['user_mentions'] is not None:
                    for j in range(len(entity_field['user_mentions'])):
                        if entity_field['user_mentions'][j]['screen_name'].lower() == keywords[i].lower():
                            self.tweet_flag = 1
                            break
                if entity_field['urls'] is not None and self.tweet_flag == 0:
                    for j in range(len(entity_field['urls'])):
                        if entity_field['urls'][j]['expanded_url'].lower() in keywords[i].lower():
                            self.tweet_flag = 1
                            break
                if "media" in entity_field and self.tweet_flag == 0:
                    for j in range(len(entity_field['media'])):
                        if entity_field['media'][j]['expanded_url'].lower() in keywords[i].lower():
                            self.tweet_flag = 1
                            break
                if self.tweet_flag == 1:
                    break
            if self.tweet_flag == 1:
                self.tweet_count = self.tweet_count + 1
                msg = filter(lambda x: x in string.printable, message)
                print "\n"+msg+"\n"                
                try:
                    #write out to kafka topic
                    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
                    future = producer.send(mytopic, (str(json.dumps(status._json, indent=4))+"\n"))
                    record_metadata = future.get(timeout=10)
                    print record_metadata.topic
                    print record_metadata.partition
                    print record_metadata.offset
                except Exception, e:
                    print str(e)
                    return True
            self.tweet_flag = 0
        else:
            return False        
                
        return True

 
    def on_error(self, status_code):

        print('Got an error with status code: ' + str(status_code))
        return False # To stop listening
 
    def on_timeout(self):

        print('Timeout...')
        return False # To stop listening


def streamTwitter(keywordargs,latlngs,topic_name):
    
    for existing_streams in streams:
        existing_streams.disconnect()
    del streams[:]

    global keywords
    del keywords[:]
    keywords.extend(keywordargs)

    global mytopic
    mytopic = topic_name

    listener = StdOutListener()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, listener)
    streams.append(stream)
    stream.filter(locations=latlngs,async=True)