from rest_framework import serializers
# from rest_framework import employees
from . models import ad_login_input
from rest_framework.urlpatterns import format_suffix_patterns

class loginSerializer(serializers.ModelSerializer):

    class Meta:
        model = ad_login_input
        fields = '__all__'

    def create(self, validated_data):
        return ad_login_input.objects.create(**validated_data)

