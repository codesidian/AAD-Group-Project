from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .serializers import ItemSerializer, NotificationSerializer, SaleSerializer, SaleItemSerializer, CustomerSerializer
from .models import Item, Notification, Sale, SaleItem, Customer
from .filters import SaleFilter

from rest_framework.decorators import action
from rest_framework.response import Response

from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime, timedelta


class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        SessionAuthentication,
    ]
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer
    lookup_field = 'code'

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        query = self.queryset.filter(quantity__lte=F('warning_quantity'))
        query = self.filter_queryset(query)
        seralizer = self.get_serializer(query, many=True)
        return Response(seralizer.data)
    

class SaleViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        SessionAuthentication,
    ]
    queryset = Sale.objects.all().order_by('id')
    serializer_class = SaleSerializer
    filterset_class = SaleFilter

    @action(detail=False, methods=['put'])
    def make(self, request, pk=None):
        data = request.data
        with transaction.atomic():
            sale = Sale()
            try:
                sale.customer = Customer.objects.get(
                    user_id=self.request.user.id)
            except Customer.DoesNotExist:
                return Response(status=403)
            sale.datetime = datetime.today()
            sale.save()
            for item in data['items']:
                dbitem = Item.objects.get(code=item['code'])
                quantity = max(min(item['quantity'], dbitem.quantity), 0)
                if quantity == 0:
                    continue

                dbitem.quantity -= quantity
                dbitem.save()

                saleitem = SaleItem()
                saleitem.sale = sale
                saleitem.item = dbitem
                saleitem.quantity = quantity
                saleitem.sale_price = dbitem.price
                saleitem.returned_quantity = 0
                saleitem.save()

            seralizer = self.serializer_class(sale,
                                              context={'request': request})

            return Response(seralizer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now()
        query = self.queryset.filter(datetime__year=today.year,datetime__month=today.month,datetime__day=today.day)
        seralizer = self.get_serializer(query, many=True)
        return Response(seralizer.data)
    
    @action(detail=False, methods=['get'])
    def yesterday(self, request):
        yesterday = timezone.now() - timedelta(days=1)
        query = self.queryset.filter(datetime__year=yesterday.year,datetime__month=yesterday.month,datetime__day=yesterday.day)
        seralizer = self.get_serializer(query, many=True)
        return Response(seralizer.data)
    
    # def get_queryset(self):
    #     filterDate = self.request.query_params.get('filterdate', None)
    #     dtFilterDate = parse_datetime(filterDate)
    #     if dtFilterDate is not None:
    #         queryset = queryset.filter(datetime__year=dtFilterDate.year,datetime__month=dtFilterDate.month,datetime__day=dtFilterDate.day)
    #     return queryset
    
class SaleItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        SessionAuthentication,
    ]
    queryset = SaleItem.objects.all().order_by('id')
    serializer_class = SaleItemSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        SessionAuthentication,
    ]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by('created_date')

    def list(self, request, *args, **kwargs):
        data = Notification.objects.filter(user_id=self.request.user.id,
                                           seen=False)
        serializer = NotificationSerializer(data, many=True)
        return Response(serializer.data)

    #you can switch the method to get if you want to test using /api/ page
    @action(detail=True, methods=['post'])
    def seen(self, request, pk=None):
        readNotification = Notification.objects.get(
            id=pk, user_id=self.request.user.id)
        if readNotification is not None:
            readNotification.seen = True
            readNotification.save()
            serializer = NotificationSerializer(readNotification)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        SessionAuthentication,
    ]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
