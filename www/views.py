import json
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.





def api_call_example(request):

	'''
	This is an example of an API call. In charities.urls you have
	to set up the url that will call this one
	'''	

	# Example response object
	response = { 'status':'success' }

	return HttpResponse(json.dumps(response)), content_type="application/json")
