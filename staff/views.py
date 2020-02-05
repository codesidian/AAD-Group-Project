from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from api.models import Department, Customer, User, Staff
from django.contrib import messages
from django.db import transaction
from utils.decorators import staff_required, basic_required, manager_required
# from .models import ???


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
    departments =  Department.objects.all()
    access_levels =  Staff.StaffAccessLevel.choices
    if HttpRequest.method == 'GET':
        context = {'title': 'Admin',
                'departments':departments,
                'access_levels':access_levels}
        return render(HttpRequest, 'staff/admin.html', context)

        
def isCustomerInfoValid(username,passwordA,passwordB,email,firstname,lastname,chargecode,department):
    valid = False
    if (0 < len(username) <= 150 and (passwordA == passwordB and 0 < len(passwordA) <= 128)
        and 0 < len(email) <= 254 and 0 < len(firstname) <= 30 and 0 < len(lastname) <= 30 and 0 < len(chargecode) <= 16):
        if Department.objects.get(id=department):
            valid = True
    
    return valid

def ifStaffInfoValid(username,passwordA,passwordB,email,firstname,lastname,logincode,accesslevel):
    valid = False
    if (0 < len(username) <= 150 and (passwordA == passwordB and 0 < len(passwordA) <= 128)
        and 0 < len(email) <= 254 and 0 < len(firstname) <= 30 and 0 < len(lastname) <= 30 and 0 < len(logincode) <= 16):
        if accesslevel in Staff.StaffAccessLevel.values:
            valid = True
    
    return valid

@login_required
def createCustomer(HttpRequest):
    if HttpRequest.method == 'POST':
        r = HttpRequest
        if isCustomerInfoValid(r.POST['username'],r.POST['passwordA'],
                              r.POST['passwordB'],r.POST['email'],
                              r.POST['first_name'],r.POST['last_name'],
                              r.POST['charge_code'],r.POST['department']):
            with transaction.atomic():
                newUser = User.objects.create_user(username=r.POST['username'],password=r.POST['passwordA'],
                            email=r.POST['email'],first_name=r.POST['first_name'],
                            last_name=r.POST['last_name'],is_customer=True)
                newUser.save()
                cusProfile = Customer.objects.get(user_id=newUser.id)
                cusProfile.first_name = r.POST['first_name']
                cusProfile.last_name = r.POST['last_name']
                cusProfile.charge_code = r.POST['charge_code']
                cusProfile.dept_id = r.POST['department']
                cusProfile.save()
            messages.success(HttpRequest, str(r.POST['first_name'])+"'s customer account created successfully as "+str(r.POST['username']))
            return HttpResponseRedirect("admin")
        else:
            messages.error(HttpRequest, 'Customer account creation failed, please check field lengths and passwords match.')
    return HttpResponseRedirect("admin")

    
@login_required
@manager_required
def createStaff(HttpRequest):
    if HttpRequest.method == 'POST':
        r = HttpRequest
        if ifStaffInfoValid(r.POST['username'],r.POST['passwordA'],
                              r.POST['passwordB'],r.POST['email'],
                              r.POST['first_name'],r.POST['last_name'],
                              r.POST['login_code'],r.POST['access_level']):
            with transaction.atomic():
                newUser = User.objects.create_user(username=r.POST['username'],password=r.POST['passwordA'],
                email=r.POST['email'],first_name=r.POST['first_name'],
                last_name=r.POST['last_name'],is_customer=False)
                newUser.save()
                staffProfile = Staff.objects.get(user_id=newUser.id)
                staffProfile.first_name = r.POST['first_name']
                staffProfile.last_name = r.POST['last_name']
                staffProfile.login_code = r.POST['login_code']
                staffProfile.access_level = r.POST['access_level']
                staffProfile.save()
            messages.success(HttpRequest, str(r.POST['first_name'])+"'s staff account created successfully as "+str(r.POST['username']))
            return HttpResponseRedirect("admin")
        else:
            messages.error(HttpRequest, 'Staff account creation failed, please check field lengths and passwords match.')
    return HttpResponseRedirect("admin")
