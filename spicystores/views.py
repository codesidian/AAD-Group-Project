from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

def home(request):
   if request.user.is_authenticated:
    #models/database aren't complete yet
    if request.user.is_customer:
      return HttpResponseRedirect("/customer")
    else:
      return HttpResponseRedirect("/staff")

   else:
      return render(request,'login.html');

def user_auth(request):
   print("Authenticating...")
   try:
      password = request.POST['password']
      username = request.POST['username']
   except KeyError:
      print("Failed to authenticate!")
      return HttpResponseRedirect("/")
   user = authenticate(request, username=username, password=password)
 
   if user is not None:
      print("Logging In...")
      login(request,user)
      print("Redirecting...")
      #Check if the user is a customer, and redirect as appropriate
      if user.is_customer:
         return HttpResponseRedirect("/customer")
      else:
         return HttpResponseRedirect("/staff")
   else:
      print("Failed to authenticate!")
      return HttpResponseRedirect("/")

def user_logout(HttpRequest):
   print("User logged out " +  HttpRequest.session["username"])
   logout(HttpRequest)
   return HttpResponseRedirect('/')

