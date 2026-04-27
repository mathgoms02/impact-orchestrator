from rest_framework import serializers
from .models import Voluntario, Crise, Perfil
from django.contrib.auth.models import User

class VoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voluntario
        fields = '__all__'

class CriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crise
        fields = '__all__'