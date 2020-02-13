from django_filters import rest_framework as filters
from .models import *

class SaleFilter(filters.FilterSet):
    date = filters.DateFilter(field_name='datetime', method='check_date')

    def check_date(self, queryset, name, value):
        return queryset.filter(datetime__date=value)
