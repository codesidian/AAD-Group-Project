from background_task import background
from django.conf import settings
from api.models import Notification, Sale, SaleItem, Item, Customer
from openpyxl import Workbook
import uuid
#TODO: Connect with background tasks for background processing

@background(schedule=60)
def generateSalesReport(userId,fromDate,toDate):
    thisWeeksSales = Sale.objects.filter(datetime__range=[fromDate, toDate])
    headers = ['ID','Date','Customer Name','Quantity','Price']
    wb = Workbook()
    ws1 = wb.active
    #Sheet 1 sales report overview
    ws1.title = "Sales Report Overview" 
    ws1.append(headers)
    for sale in thisWeeksSales:
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
    for sale in thisWeeksSales:
        saleItems = SaleItem.objects.filter(sale_id=sale.id)
        currentPrice = 0
        currentQuantity = 0
        customer = Customer.objects.get(user_id=sale.customer_id)
        for items in saleItems:
            itemDetails = Item.objects.get(id=items.item_id)
            currentRow = [sale.id,itemDetails.code,itemDetails.name,items.quantity,items.sale_price,items.returned_quantity,sale.datetime,customer.dept_id,customer.full_name]
            ws2.append(currentRow)
    wb.save("week_sales_"+str(uuid.uuid4())+".xlsx")
    


    reportMessage="Weekly Sales Report"

    notify = Notification(user_id=userId,text=reportMessage,notification_type="RE",link="NotImplemented",seen=False)
    notify.save()
        

def generateReturnsReport(userid):
    return NotImplementedError

def resetPasswordEmail(userid):
    #ask for email
    #new pass
    return NotImplementedError