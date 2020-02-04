from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
import api.models
# from .models import ???
# Create your views here.
@login_required
def home(HttpRequest):

    context = {'title': 'Staff Home'}
    return render(HttpRequest, 'staff/home.html', context)


@login_required
def products(HttpRequest):
    context = {'title': 'Products'}
    return render(HttpRequest, 'staff/products.html', context)

@login_required
def reports(HttpRequest):
    context = {'title': 'Reports'}
    return render(HttpRequest, 'staff/reports.html', context)

@login_required
def sales(HttpRequest):
    context = {'title': 'Sales'}
    return render(HttpRequest, 'staff/sales.html', context)

@login_required
def intelligence(HttpRequest):
    context = {'title': 'Intelligence'}
    return render(HttpRequest, 'staff/intelligence.html', context)

@login_required
def admin(HttpRequest):
    context = {'title': 'Admin'}
    return render(HttpRequest, 'staff/admin.html', context)
