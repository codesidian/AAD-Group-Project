from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'notifications', views.NotificationViewSet, basename="notifications")
router.register(r'sales', views.SaleViewSet)
router.register(r'sale_items', views.SaleItemViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'reports', views.ReportViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path(
        'api-auth/',
        include(
            'rest_framework.urls',
            namespace='rest_framework'
        )
    )
]
