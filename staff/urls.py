from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="staffmodule-home"),
    #path('add', views.add, name="staffmodule-add"),
]
