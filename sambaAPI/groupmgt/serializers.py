from rest_framework import serializers
from .models import grpmgmt, grpmembers

class grpmgmtserializer(serializers.ModelSerializer):
    class Meta:
        managed = False
        model = grpmgmt
        fields = '__all__'


class grpmembersserializer(serializers.ModelSerializer):
    class Meta:
        managed = False
        model = grpmembers
        fields = '__all__'
