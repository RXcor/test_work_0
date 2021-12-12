from rest_framework.serializers import ModelSerializer
from .models import Record

class RecordSerializer(ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Record