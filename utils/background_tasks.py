#from background_task import background
from django.conf import settings
from api.models import Notification, Sale, SaleItem, Item, Customer
from openpyxl import Workbook
import uuid
#TODO: Connect with background tasks for background processing
#@background(shedule=60)
def generateSalesReport(userId,fromDate,toDate):
    thisWeeksSales = Sale.objects.filter(datetime__range=[fromDate, toDate])
    headers = ['ID','Date','Customer Name','Quantity','Price']
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Weekly Sales Report" 
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
    wb.save("week_sales_"+str(uuid.uuid4())+".xlsx")
    return 0
    #TODO: Genereate detailed report on sheet 2
    #SaleItem sheet
    ws2 = wb.create_sheet(title="Weekly Sales Item Report")

    wb.save("sample.xlsx")
    reportMessage="Weekly Sales Report"
    
    #TODO: generate links for reports via routes
    notify = Notification(user_id=userId,text=reportMessage,notification_type="RE",link="NotImplemented")
    
        

def generateReturnsReport(userid):
    return NotImplementedError