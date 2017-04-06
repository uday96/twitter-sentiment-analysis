from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import StreamFilterInputForm
from twitter_streaming import streamTwitter
import re, json
from kafka import KafkaConsumer
from twitter_streaming import mytopic

class Home(View):

	def get(self,request):
		print "Home Page!"
		return redirect("/tweets/")

class StreamTweets(View):

	template_name = "filterinput.html"

	def get(self,request):
		print "Stream Tweets GET"
		form = StreamFilterInputForm()
		return render(request,self.template_name,{'header' : "Filter Tweets!!",'form' : form })

	def post(self, request, **kwargs):
		print "Stream Tweets POST"
		form = StreamFilterInputForm(request.POST)
		if form.is_valid():
			print 'valid form'
			keywords = form.cleaned_data['Keywords']	
			location = form.cleaned_data['Location']
			latlng_string = form.cleaned_data['LatLng']
			print "Location : "+location+"\n"+str(latlng_string)
			keywords = keywords.split('\r\n')
			print "KeyWords : "+str(len(keywords))
			topic_name = ""
			for word in keywords:
				print "	"+word
				topic_name = topic_name+word+"_"
			topic_name = topic_name+location
			latlng_pairs = re.findall('(\(.+?\))',latlng_string[1:-1])
			latlng_bounds=[]
			for latlng_pair in latlng_pairs:
				latlngs = latlng_pair[1:-1].split(',')
				latlng_bounds.append(float(latlngs[1]))
				latlng_bounds.append(float(latlngs[0]))
			print latlng_bounds
			topic_name = topic_name.replace(" -  ","_")
			topic_name = topic_name.replace(" ","_")
			print "\n"+topic_name+"\n"
			streamTwitter(keywords,latlng_bounds,topic_name)
			return redirect("/tweets/visualise?topic="+topic_name)

class VisualiseTweets(View):

	template_name = "map.html"

	def get(self,request):
		print "Visualise Tweets GET"
		topic_name = request.GET.get("topic",None)
		if not topic_name:
			return HttpResponse("Invalid Topic Name!")
		print "Topic: "+topic_name
		return render(request,self.template_name)


def createHTML(tweet):
	contentString = '<div class="infowindow-content"><blockquote class="twitter-tweet" lang="en"><p>'
	contentString = contentString + tweet["text"]+'</p>&mdash; '
	contentString = contentString + tweet["user"]["name"] +' (@'+tweet["user"]["screen_name"]+')'
	contentString = contentString + ' <a href="https://twitter.com/'+tweet["user"]["screen_name"]+'/statuses/'+tweet["id_str"]+'">'
	contentString = contentString + '</a></blockquote></div>'
	print "\n"+contentString+"\n"
	return contentString

class ConsumeTweets(View):

	def get(self,request):
		print "Consume Tweets GET"
		topic_name = request.GET.get("topic",None)
		if not topic_name:
			return JsonResponse({'count': 0,'data': [],'error':"Invalid Topic"})
		print "Topic: "+topic_name
		consumer = KafkaConsumer(topic_name,bootstrap_servers=['localhost:9092'])
		i=0
		polled = consumer.poll(100,None)
		while(bool(polled)==False):
			polled = consumer.poll(100,None)
			i = i+1
			if(i>10):
				break
		msgs=[]
		for key in polled.keys():
			if key.topic==mytopic:
				msgrecords = polled.get(key,[])
				for record in msgrecords:
					tweet = json.loads(record.value)
					try:
						tweet_html = createHTML(tweet)
						tweet["embeddedTweet"] = tweet_html
					except Exception as e:
						print str(e)
					msgs.append(tweet)
		consumer.close()
		return JsonResponse({'count': len(msgs),'data': msgs,'error':"None"})



