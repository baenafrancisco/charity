import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.





def api_call_example(request):

	'''
	This is an example of an API call. In charities.urls you have
	to set up the url that will call this one
	'''	
	anothevar = 2
	# Example response object
	response = { 'status':'success' ,
				'avddd' : anothevar }
	return HttpResponse(json.dumps(response), content_type="application/json")



def api_call_example2(request):

	'''
	This is an example of an API call. In charities.urls you have
	to set up the url that will call this one
	'''	

	user_balances = []
	for profile in UserProfile.objects.all():

		
		user_balances.append({profile.user.username : profile.balance})

	# Example response object
	response = { 'status':'success' ,
				'user_balances' : user_balances }
	return HttpResponse(json.dumps(response), content_type="application/json")
