from rest_framework import serializers
from .models import Item


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
