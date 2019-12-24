from rest_framework import serializers
from .models import UsersModel, UserReport

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        managed=False
        model = UsersModel
        fields = '__all__'


# class UserPasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         managed=False
#         model = UserPassword
#         fields = '__all__'

class UserReportSerializer(serializers.ModelSerializer):
    class Meta:
        managed=False
        model = UserReport
        fields = '__all__'

