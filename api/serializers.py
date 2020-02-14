from rest_framework import serializers
from .models import Item, Notification, Sale, SaleItem, Customer, Report, Staff


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'code', 'name', 'price', 'quantity',
                  'warning_quantity', 'is_chemical', 'pack_size', 'for_sale')
        lookup_field = 'code'


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user_id', 'text', 'created_date', 'notification_type',
                  'link', 'seen')


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SlugRelatedField(queryset=Item.objects.all(),
                                        slug_field='code')
    item_name = serializers.StringRelatedField(source='item')

    class Meta:
        model = SaleItem
        fields = (
            'id',
            'item',
            'sale_price',
            'quantity',
            'returned_quantity',
            'item_name',
        )


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    saleitem_set = SaleItemSerializer(many=True)
    customer = serializers.StringRelatedField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'datetime',
            'customer',
            'customer_id',
            'saleitem_set',
        )


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = (
            'user_id',
            'first_name',
            'last_name',
            'charge_code',
            'pays_vat',
            'allowed_chemicals',
        )

class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = (
            'id',
            'filename',
            'report_type',
            'created_date'
        )
