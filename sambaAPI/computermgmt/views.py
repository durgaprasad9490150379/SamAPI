from .serializers import ComputerMgmtSerializer, ComputerReportSerializer
from rest_framework.response import Response
from .models import ComputerMgmt, ComputerReport
from rest_framework import status
import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.decorators import api_view, renderer_classes,permission_classes, schema

from sambaAPI.services.CMService import  CMServices
from sambaAPI.services.connection import ConnectionService


custom_schema = AutoSchema(manual_fields=[
 	coreapi.Field("computer_name",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("domain_container",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("description",required=True,location="form",schema=coreschema.String()),
	])

move_schema = AutoSchema(manual_fields=[
        coreapi.Field("computer_name",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("domain_container",required=True,location="form",schema=coreschema.String()),
        ])

@api_view(['POST'])
@schema(custom_schema)
def create(request, format=None):
    print(request.data)
    cm = ComputerMgmt()
    if request.data != {}:
        cm.computer_name=request.data['computer_name']
        cm.domain_container=request.data['domain_container']
        cm.description=request.data['description']
        response = CMServices(ConnectionService('exza')).create(cm=cm, request= request.data)
        return Response(response.status)
    return Response("Invalid Computer data")

@api_view(['DELETE'])
def delete(request,computer_name,format=None):
    response = CMServices(ConnectionService('exza')).delete(computer_name = computer_name,force_subtree_delete=False)
    return Response(response.status)


@api_view(['GET'])
def list(request, format=None):
    response = CMServices(ConnectionService('exza')).list()
    if response.data is None:
        return Response(response.status)
    comp_list = []
    for msg in response.data:
        print(msg)
        comp_report = ComputerReport()
        comp_report.name = msg.get('name')
        comp_report.dn = msg.get('dn')
        # compreport.objectClass = msg.get('objectClass')
        comp_report.cn = msg.get('cn')
        comp_report.sn = msg.get('sn')
        comp_report.description = msg.get('description')
        comp_report.instanceType = msg.get('instanceType')
        comp_report.whenCreated = msg.get('whenCreated')
        comp_report.whenChanged = msg.get('whenChanged')
        comp_report.uSNCreated = msg.get('uSNCreated')
        comp_report.badPwdCount = msg.get('badPwdCount')
        comp_report.codePage = msg.get('codePage')
        comp_report.countryCode = msg.get('countryCode')
        comp_report.badPasswordTime = msg.get('badPasswordTime')
        comp_report.lastLogoff = msg.get('lastLogoff')
        comp_report.lastLogon = msg.get('lastLogon')
        comp_report.primaryGroupID = msg.get('primaryGroupID')
        comp_report.accountExpires = msg.get('accountExpires')
        comp_report.logonCount = msg.get('logonCount')
        comp_report.sAMAccountName = msg.get('sAMAccountName')
        comp_report.sAMAccountType = msg.get('sAMAccountType')
        comp_report.objectCategory = msg.get('objectCategory')
        comp_report.pwdLastSet = msg.get('pwdLastSet')
        comp_report.userAccountControl = msg.get('userAccountControl')
        comp_report.isCriticalSystemObject = msg.get('isCriticalSystemObject')
        comp_report.uSNChanged = msg.get('uSNChanged')
        comp_report.distinguishedName = msg.get('distinguishedName')

        comp_list.append(comp_report)
    print(response.data)
    serializer = ComputerReportSerializer(comp_list, many=True)    
    return Response(serializer.data,response.status)



@api_view(['GET'])
def show(request,computer_name,format=None):
    print(computer_name)
    response = CMServices(ConnectionService('exza')).show(computer_name=computer_name)
    if response.data is None:
        return Response("No records")
    comp_list = []
    for msg in response.data:
        print(msg)
        comp_report = ComputerReport()
        comp_report.name = msg.get('name')
        comp_report.dn = msg.get('dn')
        # compreport.objectClass = msg.get('objectClass')
        comp_report.cn = msg.get('cn')
        comp_report.sn = msg.get('sn')
        comp_report.description = msg.get('description')
        comp_report.instanceType = msg.get('instanceType')
        comp_report.whenCreated = msg.get('whenCreated')
        comp_report.whenChanged = msg.get('whenChanged')
        comp_report.uSNCreated = msg.get('uSNCreated')
        comp_report.badPwdCount = msg.get('badPwdCount')
        comp_report.codePage = msg.get('codePage')
        comp_report.countryCode = msg.get('countryCode')
        comp_report.badPasswordTime = msg.get('badPasswordTime')
        comp_report.lastLogoff = msg.get('lastLogoff')
        comp_report.lastLogon = msg.get('lastLogon')
        comp_report.primaryGroupID = msg.get('primaryGroupID')
        comp_report.accountExpires = msg.get('accountExpires')
        comp_report.logonCount = msg.get('logonCount')
        comp_report.sAMAccountName = msg.get('sAMAccountName')
        comp_report.sAMAccountType = msg.get('sAMAccountType')
        comp_report.objectCategory = msg.get('objectCategory')
        comp_report.pwdLastSet = msg.get('pwdLastSet')
        comp_report.userAccountControl = msg.get('userAccountControl')
        comp_report.isCriticalSystemObject = msg.get('isCriticalSystemObject')
        comp_report.uSNChanged = msg.get('uSNChanged')
        comp_report.distinguishedName = msg.get('distinguishedName')

        comp_list.append(comp_report)
    print(response.data)
    serializer = ComputerReportSerializer(comp_list, many=True)    
    return Response(serializer.data,response.status)



# @api_view(['PUT'])
# @schema(move_schema)
# def move(request,computer_name,format=None):
#     # cm = ComputerMgmt()
#     # cm.computer_name = computer_name
#     response = CMServices(ConnectionService('exza')).rename(computer_name = computer_name, request=request.data)
#     print(computer_name)
#     print(request.data['domain_container'])
#     return Response(response.status)


@api_view(['PUT'])
@schema(move_schema)
def move(request,format=None):
    computer_name = request.data['computer_name']
    domain_container = request.data['domain_container']
    if request.data != {}:
        if(computer_name == '' or domain_container == ''):
            return Response("Fields cannot be empty!!")
        else:
            computer_list = computer_name.split(',')
            print(len(computer_list))
            count = 0
            for i in range(0, len(computer_list)):
                print(computer_list[i])
                response = CMServices(ConnectionService('exza')).rename(computer_name = computer_list[i], domain_container= domain_container)
                if(response.status == 200):
                    count = count + 1
            return Response("In testing")
    else:
        return Response("Invalid data")



    
    # computer_list = []

    # response = CMServices(ConnectionService('exza')).rename(computer_name = computer_name, request=request.data)
    # print(computer_name)
    # print(request.data['domain_container'])
    # return Response(response.status)

