from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import StreamFilterInputForm
from twitter_streaming import streamTwitter
import re

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
			for word in keywords:
				print "	"+word
			latlng_pairs = re.findall('(\(.+?\))',latlng_string[1:-1])
			latlng_bounds=[]
			for latlng_pair in latlng_pairs:
				latlngs = latlng_pair[1:-1].split(',')
				latlng_bounds.append(float(latlngs[1]))
				latlng_bounds.append(float(latlngs[0]))
			print latlng_bounds
			streamTwitter(keywords,latlng_bounds)
		return HttpResponse("Filtered Tweets!!")