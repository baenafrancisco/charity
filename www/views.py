# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import *

'''
HELPER FUNCTIONS
'''

def get_user_profile_or_create(user):
	'''
	Some more Hackathon Code :)
	Gets an user profile or creates one with £5 of balance
	'''
	try:
		profile = UserProfile.objects.get(user=user)
	except:
		profile = UserProfile(user=user, balance=5)

	return profile


'''
VIEW FUNCTIONS
'''


def home(request):
	"""
	Displays the homepage
	"""

	context = { 'name':'darryl'}
	f = UserProfile.objects.get(user=request.user)

	# one line comment

	'''
	Many many lines 
	'''
	return render(request,'home.html', context)


def display_user_profile(request, user_id):
	"""
	Displays an user profile, user #1 if there's an error
	"""
	try:
		user = User.objects.get(pk=user_id)
	except:
		user = User.objects.get(pk=1)
		
	# Get the user profile
	profile  = get_user_profile_or_create(user)

	context = { 'user_full_name': user.get_full_name(),
				'user_top_charities':["British Heart Foundation","Cancer Research UK", "Red Cross"], #TODO: implement top charities
				'user_total_donations':profile.number_of_donations(),
				'user_ammount_donated':profile.ammount_donated(),
				'user_friend_ranking':10,
				'user_world_ranking':4096
	}
	
	return render(request,'user_profile.html', context)


def display_charity_profile(request, charity_id):
	"""
	Displays a charity profile, #1 if there's an error
	"""
	try:
		charity = Charity.objects.get(pk=charity_id)
	except:
		charity = Charity.objects.get(pk=2)

	# Create images list
	images = []
	for image in charity.images.all():
		images.append(image.url)

	context = {
		'charity_name':charity.name,
		'charity_description': charity.description,
		'charity_id': charity.pk,
		'charity_images':images,
		'charity_top_donors': ["Bob","Fred","Jeff"],
	}

	return render(request,'charity_profile.html', context)



def get_next_charities(request):
	'''
	[GET] - /api/getnextcharities/

	-Parameters
	n (=10): number of charities

	-Response

	Returns next n charities.
	If n is not specified, returns 10. If there are not more charities, returns an empty list ([]).
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

@csrf_exempt
def donate_to_charity(request):
	'''
	[POST] - /api/donatetocharity/

	-Parameters
		id : id of the charity to donate. Compulsory.

	-Response

	The response will be an object a status variable. The status can be one of the 4 following:
		-success: 10 pence have been donated to the charity specified
		-no_more_credit: the user has not enough credit to make donations
		-bad_request: id parameter hasn’t been specified in the request
		-failure: something (guess what) went wrong

	'''

	response = {"status":"bad_request"}
	# If the id var is in the POST variable

	if 'id' in request.POST:
		try:
			charity = Charity.objects.get(id=request.POST['id'])
			user_profile = UserProfile.objects.get(user=request.user)
			if user_profile.balance>=0.10:
				user_profile.seen.add(charity)
				user_profile.balance = user_profile.balance - 0.1
				user_profile.save()

				donation = Donation(user=request.user, ammount=0.10, charity=charity)
				donation.save()
				response["status"]="success"

			else:
				response["status"]="no_more_credit"
		except:
			response["status"]="failure"

	# TODO: implement donate_to_charity logic

	# We return an HTTP response with the information in JSON
	return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def decline_donation(request):
	'''
	[POST] - /api/declinedonation/

	-Parameters
		id : id of the charity to decline donation. Compulsory.


	-Response

	The response will be an object a status variable. The status can be one of the 3 following:
		-success: the record has been correctly
		-bad_request:  id parameter hasn’t been specified in the request
		-failure: some error happened

	'''

	response = {"status":"bad_request"}
	# If the id var is in the POST variable

	if 'id' in request.POST:
		try:
			charity = Charity.objects.get(id=request.POST['id'])
			user_profile = UserProfile.objects.get(user=request.user)
			user_profile.seen.add(charity)
			user_profile.save()
			response["status"]="success"
			
		except:
			response["status"]="failure"

	# We return an HTTP response with the information in JSON
	return HttpResponse(json.dumps(response), content_type="application/json")

