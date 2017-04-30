Twitter Play - Kafka
======================
Twitter Play - Kafka filters the real-time tweets based on the keywords and location (Latitude, Longitude bounds) provided. Later, the filtered tweets are visualised on a Map with respect to their Geolocation. 

#Overview and Specifications
Framework :
	Django - python
APIs :
	Kafka - A distributed streaming platform
	Tweepy - An easy to use python library to access Twitter API
	Google Maps API - Map interface for location filtering 

The application provides an interface for the users to input :
	Keywords : The multiple keywords to match for while filtering real time tweets taken as a word per line input.
	
	Location : The latitude & longitude bounds , the real time tweet must fall in, choosed through the Google Maps API by drawing a rectangle on the map.

Stream Listener is created using tweepy module which listens to all location filtered tweets. The location filtered tweets are matched for keywords and if matched are pushed to Kafka through its producer and auto creating a topic based on inputs. Kafka acts like a distributed message queue to which we can publish and subscribe records.The tweets are pushed as json object into the kafka topic with name “keyword_LocationName”. The filtered tweets from kafka are later consumed and visualised on a map dropping a marker for each tweet and and info window displaying the tweet’s content based on the source of the tweet.

###########################################
### Setup a kafka environment to use.
###########################################

#Start a zookeeper server (basic)
bin/zookeeper-server-start.sh config/zookeeper.properties

#Now start the Kafka server (basic):
bin/kafka-server-start.sh config/server.properties

#Create a topic
#topic named test in this script
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
#See that topic if we run the list topic command
bin/kafka-topics.sh --list --zookeeper localhost:2181

#Alternatively, instead of manually creating topics you can also configure your brokers to auto-create topics when a non-existent #topic is published to.

#Start a producer for topic test.
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test 

#Start a consumer to see data from producer.
bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic ipl_t20_India_Madhya_Pradesh --from-beginning
