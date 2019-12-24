from django.shortcuts import render

# Create your views here.

from .serializers import grpmgmtserializer, grpmembersserializer
from rest_framework.response import Response
from .models import grpmgmt, grpmembers
from rest_framework import status
import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.decorators import api_view, renderer_classes,permission_classes, schema

from sambaAPI.services.GrpService import GrpService
from sambaAPI.services.connection import ConnectionService



custom_schema = AutoSchema(manual_fields=[coreapi.Field("name",required=True,location="form",schema=coreschema.String()), 
	coreapi.Field("description",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("container",required=True,location="form",schema=coreschema.String()),
	])


create_schema = AutoSchema(manual_fields=[coreapi.Field("name",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("description",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("container",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("mail_id",required=True,location="form",schema=coreschema.String()),
#	coreapi.Field("group_type",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("notes",required=True,location="form",schema=coreschema.String()),
        ])

add_members_schema = AutoSchema(manual_fields=[coreapi.Field("groupname", required=True,location="form",schema=coreschema.String()),
	coreapi.Field("listofnames",required=True,location="form",schema=coreschema.String()),
	])

#list_members_schema = AutoSchema(manual_fields=[coreapi.Field("name",required=True,location="form",schema=coreschema.String()),
#	])

remove_members_schema = AutoSchema(manual_fields=[coreapi.Field("groupname", required=True,location="form",schema=coreschema.String()),
	coreapi.Field("listofnames",required=True,location="form",schema=coreschema.String()),
	])



@api_view(['GET'])
def list(request, format=None):
    response = GrpService(ConnectionService('exza')).list()
    grps = []
    if response.data is None:
        print(response.description)
        return Response(response.description, status=response.status)
    for msg in response.data:
        print(msg)
        grp = grpmgmt()
        grp.name = msg.get('name')
        grp.description = msg.get('description')
        grp.container = msg.get('dn')
        grp.group_type = msg.get('group_type')
        grp.group_scope = msg.get('group_scope')
        grp.mail_id = msg.get('mail')
        grp.notes = msg.get('info')
        grps.append(grp)
    serializer = grpmgmtserializer(grps, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
#@schema(list_members_schema)
def list_members(request, name, format=None):
    response = GrpService(ConnectionService('exza')).list_members(name=name)
    if response.data is None:
        print(response.description)
        return Response(response.description, status=response.status)
    mems = []
    for msg in response.data:
        gm = grpmembers()
        gm.name = msg.get('name')
        mems.append(gm)
    print(response.description, response.status)
    serializer = grpmembersserializer(mems, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@schema(create_schema)
def create(request, format=None):
    print(request.data)
    gp = grpmgmt()
    if request.data != {}:
        if request.data['name'] != '':
            gp.name = request.data['name']
        else:
            return Response("group_name should not be empty",status=status.HTTP_400_BAD_REQUEST)
#        if request.data['description'] != '':
        gp.description = request.data['description']
#        else:
#            return Response("description should not be empty", status=status.HTTP_400_BAD_REQUEST)
        if request.data['container'] != '':
            gp.container = request.data['container']
        else:
            return Response("container should not be empty", status=status.HTTP_400_BAD_REQUEST)
#        gp.group_type = request.data['group_type']
        gp.mail_id = request.data['mail_id']
        gp.notes = request.data['notes']
    else:
        return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
    response = GrpService(ConnectionService('exza')).create(grp=gp,request=request.data)
    return Response(response.description,response.status)


@api_view(['DELETE'])
def delete(request, name, format=None):
    print("In delete: " + name)
    response = GrpService(ConnectionService('exza')).delete(name=name)
    return Response(response.description, response.status)
    #return Response("In Tesing")

@api_view(['POST'])
@schema(add_members_schema)
def add_members(request, format=None):
    gp = grpmgmt()
    if request.data != {}:
        if request.data['groupname'] != '':
            if request.data['listofnames'] != '':
                response = GrpService(ConnectionService('exza')).add_members(request=request.data)
            else:
                return Response(response.description, response.status)
        else:
            return Response(response.description, response.status)
    else:
        return Response(response.description, response.status)
    return Response(response.description, response.status)

@api_view(['DELETE'])
@schema(remove_members_schema)
def remove_members(request, format=None):
    if request.data != {}:
        if request.data['groupname'] != '':
            if request.data['listofnames'] != '':
                response = GrpService(ConnectionService('exza')).remove_members(request=request.data)
            else:
                return Response(response.description, response.status)
        else:
            return Response(response.description, response.status)
    else:
        return Response(response.description, response.status)
    return Response(response.description, response.status)

@api_view(['GET'])
def show(request, name, format=None):
    response = GrpService(ConnectionService('exza')).show(name=name)
    grps = []
    for msg in response.data:
        print(msg)
        grp = grpmgmt()
        grp.name = msg.get('name')
        grp.description = msg.get('description')
        grp.container = msg.get('dn')
        grp.group_type = msg.get('group_type')
        grp.group_scope = msg.get('group_scope')
        grp.mail_id = msg.get('mail')
        grp.notes = msg.get('info')
        grps.append(grp)
    serializer = grpmgmtserializer(grps, many=True)
    return Response(serializer.data, response.status)