import django_filters
from .models import *
from django_filters import DateFilter


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    product_name = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains')  # Filter by product name

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created', 'date_ordered', 'complete', 'transaction_id']
