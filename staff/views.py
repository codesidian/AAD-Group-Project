import io
import os
import pyqrcode

from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from api.models import Department, Customer, User, Staff, Item, Report, Notification, Return, SaleItem, Sale
from utils.decorators import staff_required, basic_required, manager_required
from utils.background_tasks import generateSalesReport, generateReturnsReport, generateStockReport




@login_required
def home(HttpRequest):
    context = {'title': 'Staff Home'}
    return render(HttpRequest, 'staff/home.html', context)


@login_required
def products(HttpRequest):
    context = {'title': 'Products'}
    return render(HttpRequest, 'staff/products.html', context)


@login_required
def reports(HttpRequest,id=0):
    if HttpRequest.method == 'GET':
        filename = HttpRequest.GET.get('filename')
        print(filename)
        if filename:
            file_path = 'staff/reports/'+filename
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            messages.error(HttpRequest, 'File not found.')
            return HttpResponseRedirect("reports")
        else:
            context = {'title': 'Reports'}
            return render(HttpRequest, 'staff/reports.html', context)


@login_required
def sales(HttpRequest):
    reasons =  Return.ReturnReason.choices
    if HttpRequest.method == 'GET':
        context = {'title': 'Sales',
                'reasons':reasons}
        return render(HttpRequest, 'staff/sales.html', context)


@login_required
def intelligence(HttpRequest):
    context = {'title': 'Intelligence'}
    return render(HttpRequest, 'staff/intelligence.html', context)


@login_required
def stockCheck(HttpRequest):
    context = {'title': 'Stock Check'}
    return render(HttpRequest, 'staff/stock_check.html', context)

#TODO: Customer managemenet. Setting enabled disabled. 

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

def genSalesReport(HttpRequest):
    fromDate = timezone.now() - timedelta(days=7)
    toDate = timezone.now() 
    
    generateSalesReport(HttpRequest.user.id,str(fromDate),str(toDate))
    messages.success(HttpRequest, 'Sales report submitted.')
    return HttpResponseRedirect("reports")

def genReturnReport(HttpRequest):
    fromDate = timezone.now() - timedelta(days=7)
    toDate = timezone.now() 
    generateReturnsReport(HttpRequest.user.id,str(fromDate),str(toDate))
    messages.success(HttpRequest, 'Return report submitted.')
    return HttpResponseRedirect("reports")

def genStockReport(HttpRequest):
    fromDate = timezone.now() - timedelta(days=7)
    toDate = timezone.now() 
    generateStockReport(HttpRequest.user.id,True,str(fromDate),str(toDate))
    messages.success(HttpRequest, 'Stock report submitted.')
    return HttpResponseRedirect("reports")


@login_required
def genProductLabels(HttpRequest):
    if HttpRequest.method == 'GET':
        r = HttpRequest
        codes = r.GET.dict().values()
        items = []
        for code in codes:
            buffer = io.BytesIO()
            qr = pyqrcode.create(code, error='L', version=4)
            qr.svg(buffer, scale=7)
            itemDict = Item.objects.get(code=code).__dict__
            itemDict['price'] = "£{:.2f}".format(itemDict['price']/100)
            itemDict['qr'] = buffer.getvalue().decode('UTF-8')
            items.append(itemDict)
        context = {'items': items}
        return render(HttpRequest, 'staff/labels.html', context)

@login_required
@manager_required
def purgeReports(HttpRequest):
    if HttpRequest.method == 'POST':
        try:
            Report.objects.all().delete()
            Notification.objects.all().delete()
            messages.success(HttpRequest, 'Reports purged successfully.')
            return HttpResponseRedirect("reports")
        except:
            messages.error(HttpRequest, 'Unable to purge reports. Please try again.')
            return HttpResponseRedirect("reports")
    else:
        return HttpResponseRedirect("reports")


@login_required
def addProduct(request: HttpRequest):
    code = request.POST['code']
    name = request.POST['name']
    price = request.POST['price']
    warning_quantity = request.POST['warning_quantity']
    is_chemical = request.POST.get('is_chemical', False)
    pack_size = request.POST['pack_size']
    for_sale = request.POST.get('for_sale', False)

    item = Item()
    item.code = code
    item.name = name
    item.price = price
    item.quantity = 0
    item.warning_quantity = warning_quantity
    item.is_chemical = is_chemical
    item.pack_size = int(pack_size)
    item.for_sale = for_sale

    item.save()
    messages.success(request, 'Product: '+name+' added successfully.')
    return HttpResponseRedirect('products')


@login_required
def modifyProduct(request: HttpRequest):
    id = request.POST['id']
    code = request.POST['code']
    name = request.POST['name']
    price = request.POST['price']
    quantity = request.POST['quantity']
    warning_quantity = request.POST['warning_quantity']
    is_chemical = request.POST['is_chemical']
    pack_size = request.POST['pack_size']
    for_sale = request.POST['for_sale']

    item = None
    try:
        item = Item.objects.get(id=id)
    except Item.NotFound:
        return HttpResponse(status=404)

    item.code = code[0]
    item.name = name[0]
    item.price = int(float(price[0]) * 100)
    item.quantity = int(quantity[0])
    item.warning_quantity = int(warning_quantity[0])
    item.is_chemical = len(is_chemical) == 1
    item.pack_size = int(pack_size[0])
    item.for_sale = len(for_sale) == 1
    
    item.save()
    messages.success(request, 'Product: '+name+' changed successfully.')
    return HttpResponseRedirect('products')
@login_required
def profile(HttpRequest):
    context = {'title': 'Profile'}
    return render(HttpRequest, 'staff/profile.html', context)

@login_required
def refundProduct(request: HttpRequest):
    itemid = request.POST['item']
    refundQuantity = int(request.POST['quantity'])
    reason = request.POST['reason']
    context = {'title': 'Sales'}
    
    saleItem = SaleItem.objects.get(id=itemid)
    sale = Sale.objects.get(id=saleItem.sale_id)
    customer = Customer.objects.get(user_id=sale.customer_id)
    if(saleItem.quantity < refundQuantity):
        messages.error(request, 'Refund invalid. You can\'t refund more than the sale quantity.')
        return render(request, 'staff/sales.html', context)
    else:
        saleItem.quantity-=refundQuantity
        saleItem.returned_quantity+=refundQuantity
        ret = Return(datetime = timezone.now(), staff_id=request.user.id,
                    customer_id=customer.user_id,sale_item_id=saleItem.id,
                    reason=reason,quantity=refundQuantity)
        ret.save()
        saleItem.save()
        if(reason == 'NN' or reason == 'WI'):
            itm = Item.objects.get(id=saleItem.item_id)
            itm.quantity+=refundQuantity
            itm.save()
        messages.success(request, 'Refund created successfully.')
        return render(request, 'staff/sales.html', context)
    return render(request, 'staff/sales.html', context)

