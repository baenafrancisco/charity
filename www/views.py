import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def home(request):

	context = { 'name':'darryl'}

	# one line comment

	'''
	Many many lines 
	'''
	return render(request,'home.html', context)






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


def get_next_charities(request):

	'''
	This function should return next n (GET) charities.
	If n is not specified, default is 10
	'''


	# Get request parameters
	n = 10

	if 'n' in request.GET:
		n = request.GET['n']

	# Initialize response variable
	charities = []

	# We find the logged-in user_profile

	try:
		user_profile = UserProfile.objects.get(user=request.user)
	except:
		# Hackathon Error Handling: if there is any error
		# we will get 1st user profile
		user_profile = UserProfile.objects.get(user=1)

	# We get a random set of the next n charities 
	# that the user hasn't already seen

	remaining_charities = Charity.objects.all().order_by('?').exclude(pk__in=user_profile.seen.all())[:n]

	# And iterate through the list
	# in order to add the records to the response
	for charity in remaining_charities:
		# For that we create a new object
		new_record = {
			'id':charity.pk,
			'name':charity.name,
			'description':charity.description,
			'images':[]
		}
		# And iterate through the M2M relationship of the object
		for image in charity.images.all():
			new_record['images'].append(image.url)
		# Before exit the bucle, we add the new record to the response
		charities.append(new_record)

	# We return an HTTP response with the information in JSON
	return HttpResponse(json.dumps(charities), content_type="application/json")

