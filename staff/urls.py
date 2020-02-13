from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="staffmodule-home"),
    path('products', views.products, name="staffmodule-products"),
    path('reports', views.reports, name="staffmodule-reports"),
    path('reports/', views.reports, name="staffmodule-reportssel"),
    path('sales', views.sales, name="staffmodule-sales"),
    path('intelligence', views.intelligence, name="staffmodule-intelligence"),
    path('admin', views.admin, name="staffmodule-admin"),
    path('createcustomer', views.createCustomer, name="staffmodule-createCustomer"),
    path('createstaff', views.createStaff, name="staffmodule-createStaff"),
    path('genSalesReport',views.genSalesReport, name="staffmodule-genSalesReport"),
    path('genReturnReport',views.genReturnReport, name="staffmodule-genReturnReport"),
    path('genStockReport',views.genStockReport, name="staffmodule-genStockReport"),
    path('genProductLabels', views.genProductLabels, name="staffmodule-genProductLabels")
]
