from background_task import background
from django.conf import settings
from api.models import Notification, Sale, SaleItem, Item, Customer, Return, Staff
from openpyxl import Workbook
import uuid


@background(schedule=60)
def generateSalesReport(userid,fromDate,toDate):
    periodOfSales = Sale.objects.filter(datetime__range=[fromDate, toDate])
    headers = ['ID','Date','Customer Name','Quantity','Price']
    wb = Workbook()
    ws1 = wb.active
    #Sheet 1 sales report overview
    ws1.title = "Sales Report Overview" 
    ws1.append(headers)
    for sale in periodOfSales:
        saleItems = SaleItem.objects.filter(sale_id=sale.id)
        currentPrice = 0
        currentQuantity = 0
        for items in saleItems:
            currentPrice = currentPrice + (items.sale_price*items.quantity)
            currentQuantity = currentQuantity + items.quantity 
        customer = Customer.objects.get(user_id=sale.customer_id)
        customerName = customer.full_name
        currentRow = [sale.id,sale.datetime,customerName,currentQuantity,currentPrice]
        ws1.append(currentRow)
    #Sheet 2 sales report details
    headers = ['Sale ID','Item Code','Item Name','Quantity','Price','Returned','Date','Department','Customer Name']
    ws2 = wb.create_sheet(title="Weekly Sales Item Report")
    ws2.title = "Sales Report Details" 
    ws2.append(headers)
    for sale in periodOfSales:
        saleItems = SaleItem.objects.filter(sale_id=sale.id)
        currentPrice = 0
        currentQuantity = 0
        customer = Customer.objects.get(user_id=sale.customer_id)
        for items in saleItems:
            itemDetails = Item.objects.get(id=items.item_id)
            currentRow = [sale.id,itemDetails.code,itemDetails.name,items.quantity,items.sale_price,items.returned_quantity,sale.datetime,customer.dept_id,customer.full_name]
            ws2.append(currentRow)
    wb.save("Sales_Report"+str(uuid.uuid4())+".xlsx")
    


    reportMessage="Sales Report Ready"

    notify = Notification(user_id=userid,text=reportMessage,notification_type="RE",link="NotImplemented",seen=False)
    notify.save()
        
@background(schedule=60)
def generateReturnsReport(userid,fromDate,toDate):
    periodOfReturns = Return.objects.filter(datetime__range=[fromDate, toDate])
    headers = ['Return ID','Sale ID','Item ID','Item Name','Customer Name','Staff Name','Quantity','Reason','Date']
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Return Report" 
    ws1.append(headers)
    for ret in periodOfReturns:
        saleItem = SaleItem.objects.get(id=ret.sale_item_id)
        item = Item.objects.get(id=saleItem.item_id)
        sale = Sale.objects.get(id=saleItem.sale_id)
        staff = Staff.objects.get(user_id=ret.staff_id)
        customer = Customer.objects.get(user_id=sale.customer_id)
        currentRow = [ret.id,sale.id,item.id,item.name,customer.full_name,staff.full_name,ret.quantity,ret.reason,ret.datetime]
        ws1.append(currentRow)
    wb.save("Return_Report"+str(uuid.uuid4())+".xlsx")
    reportMessage="Return Report Ready"

    notify = Notification(user_id=userid,text=reportMessage,notification_type="RE",link="NotImplemented",seen=False)
    notify.save()

def resetPasswordEmail(userid):
    #ask for email
    #new pass
    return NotImplementedError