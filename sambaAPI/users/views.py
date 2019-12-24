from .serializers import UsersSerializer, UserReportSerializer
from rest_framework.response import Response
from .models import UsersModel, UserReport
from rest_framework import status
import coreapi, coreschema
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework.decorators import api_view, renderer_classes,permission_classes, schema

from sambaAPI.services.UserService import  UserServices
from sambaAPI.services.connection import ConnectionService


create_schema = AutoSchema(manual_fields=[
 	coreapi.Field("username",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("password",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("random_password",required=True,location="form",schema=coreschema.Boolean()),
    coreapi.Field("userou",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("surname",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("name",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("company",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("description",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("mail_address",required=True,location="form",schema=coreschema.String()),
	coreapi.Field("telephone",required=True,location="form",schema=coreschema.String()),
	])

password_set_schema = AutoSchema(manual_fields=[
 	coreapi.Field("username",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("password",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("retype_password",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("random_password",required=True,location="form",schema=coreschema.Boolean())
	])

move_schema = AutoSchema(manual_fields=[coreapi.Field("username", required=True,location="form",schema=coreschema.String()),
	coreapi.Field("new_container",required=True,location="form",schema=coreschema.String()),
	])


edit_schema = AutoSchema(manual_fields=[
 	coreapi.Field("name",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("surname",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("displayName",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("description",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("company",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("telephoneNumber",required=True,location="form",schema=coreschema.String()),
    coreapi.Field("mail",required=True,location="form",schema=coreschema.String())
    ])

password_expiry_schema =  AutoSchema(manual_fields=[
        coreapi.Field("username",required=True,location="form",schema=coreschema.String()),
        coreapi.Field("expiry_days",required=True,location="form",schema=coreschema.Integer()),
        coreapi.Field("no_expiry",required=True,location="form",schema=coreschema.Boolean()),
        ])



@api_view(['POST'])
@schema(create_schema)
def create(request, format=None):
    if request.data != {}:
        print(str(request.data))
        if((request.data['password'] != '' and request.data['random_password'] == True) or (request.data['password'] == '' and request.data['random_password'] == False)):
            return Response("Invalid password options")
        else:
            response = UserServices(ConnectionService('exza')).create(request = request.data)
        return Response(response.status)
    return Response("Bad request")
		

@api_view(['DELETE'])
def delete(request,username,format=None):
    print("In views: " + username)
    response = UserServices(ConnectionService('exza')).delete(username = username)
    return Response(response.status)


@api_view(['PUT'])
def enable(request,username,format=None):
    print("In views: " + username)
    response = UserServices(ConnectionService('exza')).user_enable(username = username)
    return Response(response.status)




@api_view(['PUT'])
def disable(request,username,format=None):
    print("In views: " + username)
    response = UserServices(ConnectionService('exza')).user_disable(username = username)
    return Response(response.status)




@api_view(['POST'])
@schema(password_expiry_schema)
def set_expiry(request, format=None):
    if request.data != {}:
        if(request.data['username'] != ''):
            if((request.data['expiry_days'] > 0 and request.data['no_expiry'] == True) or (request.data['expiry_days'] == 0 and request.data['no_expiry'] == False)):
                return Response("Invalid password options")
            else:
                response = UserServices(ConnectionService('exza')).set_expiry(request = request.data)
        else:
            return Response("Invalid username")
    else:
        return Response("Invalid data")
    return Response(response.status) 




@api_view(['GET'])
def list(request, format=None):
    response = UserServices(ConnectionService('exza')).list()
    user_services = []
    if response.data is None:
        print(response.description)
        return Response(response.description, status=response.status)
    
    for msg in response.data:
        user_report = UserReport()
        user_report.name = msg.get('name')
        # user_report.objectClass = msg.get('objectClass')   
        user_report.givenName = msg.get('givenName')
        user_report.instanceType = msg.get('instanceType')
        user_report.whenCreated = str(msg.get('whenCreated'))
        user_report.whenChanged = str(msg.get('whenChanged'))
        user_report.displayName = msg.get('displayName')
        user_report.uSNCreated = msg.get('uSNCreated')
        user_report.company = msg.get('company')
        user_report.badPwdCount = msg.get('badPwdCount')
        user_report.dn = msg.get('dn')
        user_report.description = msg.get('description')
        user_report.cn = msg.get('cn')
        user_report.sn = msg.get('sn')
        user_report.codePage = msg.get('codePage')
        user_report.countryCode = msg.get('countryCode')
        user_report.badPasswordTime = msg.get('badPasswordTime')
        user_report.lastLogoff = msg.get('lastLogoff')
        user_report.lastLogon = msg.get('lastLogon')
        user_report.primaryGroupID = msg.get('primaryGroupID')
        user_report.accountExpires = msg.get('accountExpires')
        user_report.logonCount = msg.get('logonCount')
        user_report.sAMAccountName = msg.get('sAMAccountName')
        user_report.sAMAccountType = msg.get('sAMAccountType')
        user_report.userPrincipalName = msg.get('userPrincipalName')
        user_report.objectCategory = msg.get('objectCategory')
        user_report.pwdLastSet = msg.get('pwdLastSet')
        user_report.userAccountControl = msg.get('userAccountControl')
        user_report.uSNChanged = msg.get('uSNChanged')
        user_report.mail = msg.get('mail')
        user_report.telephoneNumber = msg.get('telephoneNumber')
        # user_report.memberOf = str(msg.get('memberOf'))
        # memberOf = msg.get('memberOf')
        # print(type(memberOf))
        user_report.distinguishedName = msg.get('distinguishedName')

        user_services.append(user_report)
    serializer = UserReportSerializer(user_services, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@schema(password_set_schema)
def set_password(request, format=None):
    print(str(request.data))
    if request.data != {}:
        if request.data['username'] != '':
            if (request.data['password'] != '' and request.data['random_password'] == True) or (request.data['password'] == '' and request.data['random_password'] == False):
                return Response("Invalid password options!!")
            else:
                if(request.data['random_password'] == False):
                    if(request.data['password'] != request.data['retype_password']):
                        return Response("password mismatch")
        else:
            return Response("username can not be empty!!")
    else:
        return Response("Invalid data")

    response = UserServices(ConnectionService('exza')).set_password(request = request.data)
    return Response(response.status)



@api_view(['GET'])
def show(request, name, format=None):
    response = UserServices(ConnectionService('exza')).show(name=name)
    user_services = []
    for msg in response.data:
        user_report = UserReport()
        user_report.name = msg.get('name')
        # user_report.objectClass = msg.get('objectClass')   
        user_report.givenName = msg.get('givenName')
        user_report.instanceType = msg.get('instanceType')
        user_report.whenCreated = str(msg.get('whenCreated'))
        user_report.whenChanged = str(msg.get('whenChanged'))
        user_report.displayName = msg.get('displayName')
        user_report.uSNCreated = msg.get('uSNCreated')
        user_report.company = msg.get('company')
        user_report.badPwdCount = msg.get('badPwdCount')
        user_report.dn = msg.get('dn')
        user_report.description = msg.get('description')
        user_report.cn = msg.get('cn')
        user_report.sn = msg.get('sn')
        user_report.codePage = msg.get('codePage')
        user_report.countryCode = msg.get('countryCode')
        user_report.badPasswordTime = msg.get('badPasswordTime')
        user_report.lastLogoff = msg.get('lastLogoff')
        user_report.lastLogon = msg.get('lastLogon')
        user_report.primaryGroupID = msg.get('primaryGroupID')
        user_report.accountExpires = msg.get('accountExpires')
        user_report.logonCount = msg.get('logonCount')
        user_report.sAMAccountName = msg.get('sAMAccountName')
        user_report.sAMAccountType = msg.get('sAMAccountType')
        user_report.userPrincipalName = msg.get('userPrincipalName')
        user_report.objectCategory = msg.get('objectCategory')
        user_report.pwdLastSet = msg.get('pwdLastSet')
        user_report.userAccountControl = msg.get('userAccountControl')
        user_report.uSNChanged = msg.get('uSNChanged')
        user_report.mail = msg.get('mail')
        user_report.telephoneNumber = msg.get('telephoneNumber')

        # user_report.memberOf = str(msg.get('memberOf'))
        # memberOf = msg.get('memberOf')
        # print(type(memberOf))
        user_report.distinguishedName = msg.get('distinguishedName')

        user_services.append(user_report)
    serializer = UserReportSerializer(user_services, many=True)
    return Response(serializer.data,response.status)


@api_view(['POST'])
@schema(move_schema)
def move(request, format=None):
    if request.data != {}:
        if request.data['username'] != '':
            if request.data['new_container'] != '':
                response = UserServices(ConnectionService('exza')).move(request=request.data)
            else:
                return Response(response.description, response.status)
        else:
            return Response(response.description, response.status)
    else:
        return Response(response.description, response.status) 
    return Response(response.description, response.status)



    
# @api_view(['PUT'])
# @schema(edit_schema)
# def edit(request,username,format=None):
#     if request.data != {}:
#         if username != '':
#             response = UserServices(ConnectionService('exza')).edit_user(username = username, request = request.data)            
#         else:
#             return Response("username field cannot be empty!!")   
#     else:
#         return Response("Invalid data")
    
#     return Response(response.status)



@api_view(['PUT'])
@schema(edit_schema)
def edit(request,username,format=None):
    if username != '':
        response = UserServices(ConnectionService('exza')).show(name=username)            
    else:
        return Response("username field cannot be empty!!")
    if response.data is None:
        print(response.description)
        return Response(status=response.status)
    for msg in response.data:
        user_report = UserReport()
        user_report.dn = msg.get('dn')
        user_report.sn = msg.get('sn')
        user_report.givenName = msg.get('givenName')
        user_report.displayName = msg.get('displayName')
        user_report.description = msg.get('description')
        user_report.company = msg.get('company')
        user_report.mail = msg.get('mail')   
        user_report.telephoneNumber = msg.get('telephoneNumber')
    
    # res_string = "dn: " + dn + "\nchangetype: modify\ndelete: sn\n" + "sn:  " + sn + "\ndelete: description\n" + "description:  " + description + "\ndelete: telephoneNumber\n" + "telephoneNumber:  " + telephoneNumber + "\ndelete: givenName\n" + "givenName:  " + givenName + "\ndelete: displayName\n" + "displayName:  " + displayName + "\ndelete: company\n" + "company:  " + company + "\ndelete: mail\n" + "mail:  " + mail
    # res_string += "\nadd: sn\n" + "sn:  " + new_sn + "\nadd: description\n" + "description:  " + new_description + "\nadd: telephoneNumber\n" + "telephoneNumber:  " + new_telephoneNumber + "\nadd: givenName\n" + "givenName:  " + new_givenName + "\nadd: displayName\n" + "displayName:  " + new_displayName + "\nadd: company\n" + "company:  " + new_company + "\nadd: mail\n" + "mail:  " + new_mail

    delete_string = "dn: " + str(user_report.dn) + "\nchangetype: modify\n"
    add_string = ""

    if request.data['surname'] != '':
        if user_report.sn != None:
            delete_string += "delete: sn\n" + "sn:  " + str(user_report.sn)  + "\n"
            add_string += "add: sn\n" + "sn:  " + request.data['surname']  + "\n"
        else:
            add_string += "add: sn\n" + "sn:  " + request.data['surname']  + "\n"

    if request.data['name'] != '':
        if user_report.givenName != None:
            delete_string += "delete: givenName\n" + "givenName:  " + str(user_report.givenName)  + "\n"
            add_string += "add: givenName\n" + "givenName:  " + request.data['name']  + "\n"
        else:
            add_string += "add: givenName\n" + "givenName:  " + request.data['name']  + "\n"
    
    if request.data['description'] != '':
        if user_report.description != None:
            delete_string += "delete: description\n" + "description:  " + str(user_report.description)  + "\n"
            add_string += "add: description\n" + "description:  " + request.data['description']  + "\n"
        else:
            add_string += "add: description\n" + "description:  " + request.data['description']  + "\n"

    if request.data['displayName'] != '':
        if user_report.displayName != None:
            delete_string += "delete: displayName\n" + "displayName:  " + str(user_report.displayName)  + "\n"
            add_string += "add: displayName\n" + "displayName:  " + request.data['displayName']  + "\n"
        else:
            add_string += "add: displayName\n" + "displayName:  " + request.data['displayName']  + "\n"

    if request.data['company'] != '':
        if user_report.company != None:
            delete_string += "delete: company\n" + "company:  " + str(user_report.company)  + "\n"
            add_string += "add: company\n" + "company:  " + request.data['company']  + "\n"
        else:
            add_string += "add: company\n" + "company:  " + request.data['company']  + "\n"

    if request.data['telephoneNumber'] != '':
        if user_report.telephoneNumber != None:
            delete_string += "delete: telephoneNumber\n" + "telephoneNumber:  " + str(user_report.telephoneNumber)  + "\n"
            add_string += "add: telephoneNumber\n" + "telephoneNumber:  " + request.data['telephoneNumber']  + "\n"
        else:
            add_string += "add: telephoneNumber\n" + "telephoneNumber:  " + request.data['telephoneNumber']  + "\n"

    if request.data['mail'] != '':
        if user_report.mail != None:
            delete_string += "delete: mail\n" + "mail:  " + str(user_report.mail)  + "\n"
            add_string += "add: mail\n" + "mail:  " + request.data['mail']  + "\n"
        else:
            add_string += "add: mail\n" + "mail:  " + request.data['mail']  + "\n"

    input_string = delete_string + add_string
    response = UserServices(ConnectionService('exza')).edit_user(username= username, input_string = input_string)            
    return Response(response.status)

