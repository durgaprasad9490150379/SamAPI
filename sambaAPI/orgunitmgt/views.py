from .serializers import OrgUnitSerializer , OrgUnitReportSerializer
from rest_framework.response import Response
from .models import OrgUnit, OrgUnitReport
from rest_framework import status
import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.decorators import api_view, renderer_classes,permission_classes, schema

from sambaAPI.services.OUService import  OUService
from sambaAPI.services.connection import ConnectionService


custom_schema = AutoSchema(manual_fields=[
 	coreapi.Field("name",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("description",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("domain_name",required=True,location="form",schema=coreschema.String()),
	])

rename_schema = AutoSchema(manual_fields=[
        coreapi.Field("name",required=True,location="form",schema=coreschema.String()),
        ])

@api_view(['GET'])
def list(request, format=None):
	response = OUService(ConnectionService('exza')).list()
	ous = []
	if response.data is None:
		print(response.description)
		return Response(response.description, status=response.status)

	for msg in response.data:
		print(msg)
		ou = OrgUnitReport()
		ou.ou_name = msg.get('name')
		ou.description = msg.get('description')
		ou.domain_name = msg.get('dn')
		ou.distinguished_name = msg.get('distinguishedName')
		ou.when_changed = msg.get('whenChanged')
		ou.when_Created = msg.get('whenCreated')
		# ou.object_guid = msg.get('objectGUID')
		ou.managed_by = msg.get('managedBy')
		ous.append(ou)

	serializer = OrgUnitReportSerializer(ous, many=True)
	return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@schema(custom_schema)
def create(request, format=None):
	print(request.data)
	ou = OrgUnit()
	if request.data != {}:
		if request.data['name'] != '':
			if request.data['domain_name'] != '':
				ou.name = request.data['name']+','+request.data['domain_name']
			else:
				return Response("domain_name filed should not be empty {0}".format(request.data),status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response("name field should not be empty {0}".format(request.data), status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response("Invalid ou {0}".format(request.data), status=status.HTTP_400_BAD_REQUEST)
	ou.description = request.data['description']

	response = OUService(ConnectionService('exza')).create(ou=ou,request=request.data)

	return Response(response.description,response.status)


@api_view(['DELETE'])
def delete(request,name,format=None):
	ou = OrgUnit()
	ou.name = name
	response = OUService(ConnectionService('exza')).delete(ou=ou,force_subtree_delete=False)
	return Response(response.description,response.status)

@api_view(['put'])
@schema(rename_schema)
def rename(request,old_name,format=None):
	response = OUService(ConnectionService('exza')).rename(old_name=old_name,request=request.data)
	return Response(response.description,response.status)

@api_view(['GET'])
def edit(request,name, format=None):
	response = OUService(ConnectionService('exza')).edit(name=name)

	if response.data is None:
		return Response(response.description,response.status)
	ous = []
	for msg in response.data:
		ou = OrgUnit()
		ou.name=msg.get('name')
		ou.description=msg.get('description')
		ous.append(ou)
	serializer = OrgUnitSerializer(ous, many=True)
	return Response(serializer.data)
