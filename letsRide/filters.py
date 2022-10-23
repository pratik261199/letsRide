import django_filters
from django_filters import rest_framework as filters

from .models import RiderTravel, Requester


class RouteFilter(django_filters.FilterSet):
    class Meta:
        model = RiderTravel
        fields = []


class RequesterFilter(django_filters.FilterSet):
    class Meta:
        model = Requester
        fields = ["status", "asset_type"]
