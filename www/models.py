from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
	"""
	UserProfile is a model to store extended profile information
	of an user, as well as having functions 
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

class Charity(models.Model):
	"""
	Charity is a model to store charity information
	"""
	name = models.CharField(max_length=255)
	description = models.TextField()
	#images =  #(for the prototype, just store url(s))


	def __unicode__(self):
		return "%s" % self.name

class Donation(models.Model):
	"""
	Donation model stores information about who donates
	what quantity to which charity
	"""
	user = models.ForeignKey(User)
	ammount = models.FloatField() # TODO: use django money
	charity = models.ForeignKey(Charity)
	timestamp = models.DateTimeField(auto_now_add=True)
