from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from api.models import Department, Customer, User
from django.contrib import messages


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
#TODO: Access level decorators
def admin(HttpRequest):
    departments =  Department.objects.all()
    if HttpRequest.method == 'GET':
        context = {'title': 'Admin',
                'departments':departments}
        return render(HttpRequest, 'staff/admin.html', context)

        
def isCustomerInfoValid(username,passwordA,passwordB,email,firstname,lastname,chargecode,department):
    valid = False
    if (0 < len(username) <= 150 and (passwordA == passwordB and 0 < len(passwordA) <= 128)
        and 0 < len(email) <= 254 and 0 < len(firstname) <= 30 and 0 < len(lastname) <= 30 and 0 < len(chargecode) <= 16):
        if Department.objects.get(id=department):
            valid = True
    
    return valid

def ifStaffInfoValid(username,passwordA,passwordB,email,firstname,lastname,chargecode,department):
    valid = False
    if (0 < len(username) <= 150 and (passwordA == passwordB and 0 < len(passwordA) <= 128)
        and 0 < len(email) <= 254 and 0 < len(firstname) <= 30 and 0 < len(lastname) <= 30 and 0 < len(chargecode) <= 16):
        if Department.objects.get(id=department):
            valid = True
    
    return valid

@login_required
def createCustomer(HttpRequest):
    if HttpRequest.method == 'POST':
        departments =  Department.objects.all()
        r = HttpRequest
        if isCustomerInfoValid(r.POST['username'],r.POST['passwordA'],
                              r.POST['passwordB'],r.POST['email'],
                              r.POST['first_name'],r.POST['last_name'],
                              r.POST['charge_code'],r.POST['department']):
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
            messages.success(HttpRequest, str(r.POST['first_name'])+"'s customer created successfully as "+str(r.POST['username']))
            context = {'title': 'Admin',
                   'departments':departments}
            return render(HttpRequest, 'staff/admin.html', context)
        else:
            messages.error(HttpRequest, 'Customer account creation failed, please check field lengths and passwords match.')
    return HttpResponseRedirect("admin")

    
@login_required
def createStaff(HttpRequest):
    return NotImplemented

    if HttpRequest.method == 'POST':
        departments =  Department.objects.all()
        r = HttpRequest
        if ifStaffInfoValid(r.POST['username'],r.POST['passwordA'],
                              r.POST['passwordB'],r.POST['email'],
                              r.POST['first_name'],r.POST['last_name'],
                              r.POST['charge_code'],r.POST['department']):
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
            messages.success(HttpRequest, str(r.POST['first_name'])+"'s customer created successfully as "+str(r.POST['username']))
            context = {'title': 'Admin',
                   'departments':departments}
            return render(HttpRequest, 'staff/admin.html', context)
        else:
            messages.error(HttpRequest, 'Customer account creation failed, please check field lengths and passwords match.')
    return HttpResponseRedirect("admin")
