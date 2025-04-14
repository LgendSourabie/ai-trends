from django_filters import FilterSet
from django_filters.rest_framework import filters
from trend_app.models import Trend



class TrendFilter(FilterSet):
    megatrend = filters.CharFilter(field_name="megatrend", lookup_expr="iexact")
    macrotrend = filters.CharFilter(field_name="macrotrend", lookup_expr="iexact")
    technology_readiness_level = filters.CharFilter(field_name="technology_readiness_level", lookup_expr="iexact")

    class Meta:
        model = Trend
        fields = ['megatrend','macrotrend','technology_readiness_level']