from rest_framework import serializers
from .models import OrgUnit , OrgUnitReport

class OrgUnitSerializer(serializers.ModelSerializer):
	class Meta:
		managed=False
		model = OrgUnit
		fields = '__all__'

class OrgUnitReportSerializer(serializers.ModelSerializer):
	class Meta:
		managed=False
		model = OrgUnitReport
		fields = '__all__'
