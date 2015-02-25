from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
	"""
	UserProfile is a model to store aditional user data
	"""
	user = models.OneToOneField(User)

	'''
	Example funcitons
	def how_much_donated(self):
		# do the logic here
		# return how much an user has donated
	'''

	def __unicode__(self):
		return "%s" % self.user		

class CharityProfile(models.Model):
	"""
	CharityProfile is a model to store charity information
	"""
	name = models.CharField()

	def __unicode__(self):
		return "%s" % self.name