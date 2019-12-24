from rest_framework import serializers
from .models import ComputerMgmt, ComputerReport

class ComputerMgmtSerializer(serializers.ModelSerializer):
    class Meta:
        managed=False
        model = ComputerMgmt
        fields = '__all__'

class ComputerReportSerializer(serializers.ModelSerializer):
    class Meta:
        managed=False
        model = ComputerReport
        fields = '__all__'


