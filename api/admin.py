from django.contrib import admin
from .models import Item, User, Customer, Staff, Department, Notification, Sale, SaleItem, Return

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Department)
admin.site.register(Notification)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Return)