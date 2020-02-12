from rest_framework import serializers
from .models import Item, Notification, Sale, SaleItem


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'code',
            'name',
            'price',
            'quantity',
            'warning_quantity',
            'is_chemical',
            'pack_size',
            'for_sale'
        )
        lookup_field = 'code'

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user_id',
            'text',
            'created_date',
            'notification_type',
            'link',
            'seen'
        )


class SaleItemSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.SlugRelatedField(queryset=Item.objects.all(), slug_field='code')

    class Meta:
        model = SaleItem
        fields = (
            'item',
            'sale_price',
            'quantity',
            'returned_quantity',
        )


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    saleitem_set = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = (
            'id',
            'datetime',
            #'customer',
            'saleitem_set',
        )
