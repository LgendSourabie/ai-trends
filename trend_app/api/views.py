from django.conf import settings
from rest_framework import viewsets
from trend_app.models import Trend
from trend_app.api.serializers import TrendSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from trend_app.api.permissions import IsAdminOrReadOnly
from trend_app.api.filters import TrendFilter
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class TrendViewSet(viewsets.ModelViewSet):
    """
    View for processing trend list and detail requests 
    """
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TrendFilter
    ordering_fields=['total_count_of_publications','total_count_of_patents']
    search_fields = ['megatrend','macrotrend','technology_readiness_level']

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super(TrendViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    @action(methods=['get'], detail=False, url_path=r'megatrend=(?P<megatrend>[a-zA-Z]+)',url_name='filter_by_megatrend')
    def ai_megatrends(self, request, megatrend = None):
        """
        Filters the Megatrends and exposes them via the endpoint /trends/{megatrend} 
        """
        
        trends = self.get_queryset().filter(megatrend__iexact=megatrend)
        serializer = self.get_serializer(trends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)