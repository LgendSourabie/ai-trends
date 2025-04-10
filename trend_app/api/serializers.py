from trend_app.models import Trend
from rest_framework import serializers


class TrendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trend
        fields = "__all__"
        read_only_fields = ['uploaded_at','updated_at']