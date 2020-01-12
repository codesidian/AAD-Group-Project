from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
# from .models import ???
# Create your views here.
@login_required
def home(HttpRequest):
    # Set a session variable for username, as its not changing during their time logged in.
    HttpRequest.session["username"] = HttpRequest.user.username
    context = {'title':'Staff Home'}
    return render(HttpRequest,'staff/home.html',context)