from rest_framework import serializers
from .models import Item, Notification


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
