from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return HttpResponseRedirect('http://yapster.co');

def aws_index(request):
	return HttpResponse('Yapster, Inc.')