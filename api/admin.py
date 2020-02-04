from django.contrib import admin
from .models import Item, User, Customer, Staff, Department

admin.site.register(Item)
admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Department)
