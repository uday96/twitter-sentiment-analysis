from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from twitter_streaming import streamTwitter
from twitter_streaming import data_list
import re, json

class Home(View):

	def get(self,request):
		print "Home Page!"
		return redirect("/tweets/")

class StreamTweets(View):

	template_name = "map.html"

	def get(self,request):
		print "Stream Tweets GET"
		return render(request,self.template_name)

class ProduceTweets(View):

	def get(self,request):
		print "Produce Tweets GET"
		query = request.GET.get("query",None)
		region = request.GET.get("region",None)
		print "Query: "+query
		print "Region: "+region
		streamTwitter(query,region)
		return JsonResponse({'success': 1,'error':"None"})

class ConsumeTweets(View):

	def get(self,request):
		print "Consume Tweets GET"
		query = request.GET.get("query",None)
		print "Query: "+query
		global data_list
		n = 1
		data = data_list[:n]
		del data_list[:n]
		return JsonResponse({'count': len(data),'data': data,'error':"None"})