import django_filters
from django_filters import DateFilter,CharFilter
from .models import *


class TaskFilter(django_filters.FilterSet):
    title=CharFilter(field_name="title", lookup_expr='icontains')

    class Meta:
        model=Task
        fields=['title','category']


class PeopleFilter(django_filters.FilterSet):
    class Meta:
        model=Client
        fields=['email','id']
        