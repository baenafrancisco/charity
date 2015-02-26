from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


class UserProfile(models.Model):
	"""
	UserProfile is a model to store extended profile information
	of an user, as well as having functions 
	"""
	user = models.OneToOneField(User)
	balance = models.FloatField(default=0) # People first top up their account
	seen = models.ManyToManyField('Charity', blank=True, null=True) # Charities already seen
	#country?
	#what_else?

	'''
	Example funcitons
	def how_much_donated(self):
		# do the logic here
		# return how much an user has donated
	'''

	def donated_quantity(self):
		'''
		# Returns how much an user has donated
		'''
		response = 0
		query = Donation.objects.filter(user=self).aggregate(Sum('ammount'))['ammount__sum']
		if not query ==	None:
			response = query

		return response
		

	def __unicode__(self):
		return "%s" % self.user	

class Image(models.Model):
	"""
	Image
	"""
	url = models.URLField()
	
	def __unicode__(self):
		return "<Image: %s>" % self.url
				

class Charity(models.Model):
	"""
	Charity is a model to store charity information
	"""
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	images =  models.ManyToManyField(Image, blank=True, null=True)
	#reputation?

	def donations_received(self):
		'''
		# Returns how much an user has donated
		'''
		response = 0
		query = Donation.objects.filter(charity=self).aggregate(Sum('ammount'))['ammount__sum']
		if not query ==	None:
			response = query

		return response

	def __unicode__(self):
		return "%s" % self.name

class Donation(models.Model):
	"""
	Donation model stores information about who donates
	what quantity to which charity
	"""
	user = models.ForeignKey(User)
	ammount = models.FloatField(default=5) # TODO: use django money
	charity = models.ForeignKey(Charity)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "<Donation: %s to %s>" % (self.user, self.charity)