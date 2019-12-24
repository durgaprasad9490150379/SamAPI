from .serializers import loginSerializer
from rest_framework.response import Response
from .models import ad_login_input
from rest_framework import status
import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.decorators import api_view, renderer_classes,permission_classes, schema

from sambaAPI.services.OUService import  OUService
from sambaAPI.services.connection import ConnectionService



from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.urlpatterns import format_suffix_patterns


from ldap3 import Server, Connection, ALL

custom_schema = AutoSchema(manual_fields=[
 	coreapi.Field("username",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("password",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("domain_controller",required=True,location="form",schema=coreschema.String()),
	])

rename_schema = AutoSchema(manual_fields=[
        coreapi.Field("username",required=True,location="form",schema=coreschema.String()),
        ])


@api_view(['POST'])
@schema(custom_schema)
def create(request, format=None):
    if request.data != {}:
        if request.data['username'] != '':
            if request.data['password'] != '':
                result = check_credentials(request.data['domain_controller'], request.data['username'], request.data['password'])
                print("result: ", result)
                return Response(result)




def check_credentials(ip, username, password):
    try:
        s = Server(ip)
        connection = Connection(s, user=username, password=password)
        connection.bind()
        print(connection.result['description'])
        if connection.result['description'] == 'success':
            connection.start_tls()
            print('tls_connection_made')
        return (connection.result['description'])
    except Exception as e:
        return "invalidDomainController"

