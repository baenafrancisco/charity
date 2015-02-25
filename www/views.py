from django.shortcuts import render

def home(request):

	context = { 'name':'darryl'}

	# one line comment

	'''
	Many many lines 
	'''
	return render(request,'home.html', context)