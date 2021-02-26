from rest_framework import serializers
from .models import Salas

class SalasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Salas
        fields='__all__'