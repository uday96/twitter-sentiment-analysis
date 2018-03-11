# **Twitter - Sentiment Analysis** #

Twitter Play - Kafka filters the real-time tweets based on the keywords and location (Latitude, Longitude bounds) provided and pushes them to Kafka. The filtered tweets are then visualised on a Map with respect to their geolocation.


###**Overview and Specifications**###
-------------------
**Framework :**
> - Django-python

**APIs :**
> - **Kafka** - A distributed streaming platform
> - **Tweepy** - An easy to use python library to access Twitter API
> - **Google Maps API** - Map interface for location filtering 

The application provides an interface for the users to input :
> - **Keywords :** The multiple keywords to match for while filtering real time tweets taken as a word per line input.
> - **Location :** The latitude & longitude bounds , the real time tweet must fall in, choosed through the Google Maps API by drawing a rectangle on the map.

Stream Listener is created using tweepy module which listens to all location filtered tweets. The location filtered tweets are matched for keywords and if matched are pushed to Kafka through its producer and auto creating a topic based on inputs. Kafka acts like a distributed message queue to which we can publish and subscribe records.The tweets are pushed as json object into the kafka topic with name **keyword_LocationName**. The filtered tweets from kafka are later consumed and visualised on a map dropping a marker for each tweet and and info window displaying the tweet content based on the source of the tweet.


----------