from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import StreamFilterInputForm
from twitter_streaming import streamTwitter

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
			print "Location : "+location
			keywords = keywords.split('\r\n')
			print "KeyWords : "+str(len(keywords))
			for word in keywords:
				print "	"+word
			streamTwitter(keywords,location)
		return HttpResponse("Filtered Tweets!!")
