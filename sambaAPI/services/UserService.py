import sys
sys.path.insert(0, "/usr/local/samba/lib/python3.7/site-packages")


import samba
import ldb
import re
import difflib
from samba import dsdb
from samba import (generate_random_password)
# from samba import re
from samba.samdb import SamDB
from samba.param import LoadParm
from samba.auth import system_session
from samba.credentials import Credentials
from rest_framework import status

class UserServices:
    connection_service = None

    def __init__(self, connection):
        self.connection_service = connection


    def create(self, **kwargs):
        try:
            con = self.connection_service.connection()

        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

        request = kwargs['request']
        username = request['username']
        print(username)
        userou= "OU=" + request['userou']
        password = request['password']
        random_password = request['random_password']
        must_change_at_next_login = False
        if random_password == True:
            password = generate_random_password(128, 255)
            must_change_at_next_login = True
        print(must_change_at_next_login)

        try:
            con.newuser(username, password,  force_password_change_at_next_login_req=must_change_at_next_login,
             userou= userou, surname=request['surname'], givenname=request['name'], company= request['company'],
              telephonenumber= request['telephone'], description= request['description'], mailaddress= request['mail_address'])
        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT,'Failed to create user "%s": %s' % (request['username'], e),None)

        return ResponseStatus(status.HTTP_201_CREATED, request['username'],None)



    def delete(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e), None)
        
        username = kwargs['username']
        print("In services: " + username)
        exp = ("(&(sAMAccountName=%s)(sAMAccountType=805306368))" %
                  ldb.binary_encode(username))

        domain_dn = con.domain_dn()
        try:
            res = con.search(base= domain_dn,
                               scope=ldb.SCOPE_SUBTREE,
                               expression=exp,
                               attrs=["dn"])
            user_dn = res[0].dn

        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'unable to find user "%s": %s' % (username, e),None)

        try:
            con.delete(user_dn)
        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT, 'Failed to delete user "%s": %s' % (username, e),None)
        return ResponseStatus(status.HTTP_204_NO_CONTENT, 'user deleted successfully',None)



    def user_enable(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

        username = kwargs['username']
        print("In services: " + username)
        filter = "(&(objectClass=user)(sAMAccountName=%s))" % (ldb.binary_encode(username))
        try:
            con.enable_account(filter)
        except Exception as msg:
            return ResponseStatus(status.HTTP_409_CONFLICT,"Failed to enable user '%s': %s" % (usernamer, msg))

        return ResponseStatus(status.HTTP_200_OK,None, username)



    def user_disable(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

        username = kwargs['username']
        print("In services: " + username)
        filter = "(&(objectClass=user)(sAMAccountName=%s))" % (ldb.binary_encode(username))
        try:
            con.disable_account(filter)
        except Exception as msg:
            return ResponseStatus(status.HTTP_409_CONFLICT,"Failed to disable user '%s': %s" % (username, msg))

        return ResponseStatus(status.HTTP_200_OK,None, username)
    

    def list(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        domain_dn = con.domain_dn()
        res = con.search(domain_dn, scope=ldb.SCOPE_SUBTREE,
                           expression=("(&(objectClass=user)(userAccountControl:%s:=%u))"
                                       % (ldb.OID_COMPARATOR_AND, dsdb.UF_NORMAL_ACCOUNT)),
                           attrs=["*"])
        if(len(res) == 0):
            return ResponseStatus(status.HTTP_404_NOT_FOUND,None,None)
        print(str(res))
        for i in range(0, len(res)):
            r = str(res[i]['dn'])
            print(r)
        return ResponseStatus(status.HTTP_200_OK,None,res)



    def set_expiry(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        request = kwargs['request']
        username = request['username']
        days = request['expiry_days']
        noexpiry = request['no_expiry']
        print("In services: " + username) 

        filter = "(&(objectClass=user)(sAMAccountName=%s))" % (ldb.binary_encode(username))
        
        try:
            res = con.setexpiry(filter, days * 24 * 3600, no_expiry_req=noexpiry)
            print(str(res))
        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT,"Failed to set expiry '%s': %s" % (username, e))
            print("Unable to set expiry")
        
        if noexpiry == True:
            print("Expiry for user '%s' disabled.\n" % (
                username))
        else:
            print("Expiry for user '%s' set to %u days.\n" % (
                username , days))
        return ResponseStatus(status.HTTP_200_OK,None,res)

    def edit_user(self, **kwargs):
        try:
	        con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        res_string = kwargs['input_string']
        username = kwargs['username']
        
        try:
            print("The final string: ")
            print(res_string)
            con.modify_ldif(res_string)
        except Exception as e:
            print("exception1:  " + str(e))
            return ResponseStatus(status.HTTP_409_CONFLICT,"Failed to modify user '%s': %s" % (username, e))
        return ResponseStatus(status.HTTP_200_OK, None, None)
        

    def set_password(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        request = kwargs['request']
        username = request['username']
        password = request['password']
        random_password = request['random_password']
        must_change_at_next_login = False

        if random_password == True:
            password = generate_random_password(128, 255)
            must_change_at_next_login = True
        print(must_change_at_next_login)
        filter = "(&(objectClass=user)(sAMAccountName=%s))" % (ldb.binary_encode(username))
        exp = ("(&(sAMAccountName=%s)(sAMAccountType=805306368))" %
                  ldb.binary_encode(username))
        domain_dn = con.domain_dn()

        try:
            res = con.search(base= domain_dn,
                               scope=ldb.SCOPE_SUBTREE,
                               expression=exp,
                               attrs=["dn"])
            if(len(res) == 0):
                return ResponseStatus(status.HTTP_404_NOT_FOUND,'no user "%s"' % username,None)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'unable to find user "%s": %s' % (username, e),None)

        try:
            con.setpassword(filter, password,
                                  force_change_at_next_login=must_change_at_next_login,
                                  username=username)
        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT,None, None)
        return ResponseStatus(status.HTTP_200_OK,None,None)  



    def show(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Invalid server details "%s"' % (e), None)
        try:
            username = kwargs['name']
            filter = ("(&(sAMAccountType=%d)(sAMAccountName=%s))" %
                  (dsdb.ATYPE_NORMAL_ACCOUNT, ldb.binary_encode(username)))
            domaindn = con.domain_dn()
            res = con.search(base=domaindn, expression=filter,
                               scope=ldb.SCOPE_SUBTREE, attrs=['*'])
            if len(res) == 0:
                return ResponseStatus(status.HTTP_400_BAD_REQUEST,'User not found "%s"' % (e), None)
            user_dn = res[0].dn
            # for msg in res:
            #     user_ldif = con.write_ldif(msg, ldb.CHANGETYPE_NONE)

        except Exception as e:
            return ResponseStatus(status.HTTP_404_NOT_FOUND,'User not found "%s"' %(e), None)
        return ResponseStatus(status.HTTP_200_OK, None, res)

    def move(self, **kwargs):
        try:
            con = self. connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Invalid server details', None)
        try:
            request = kwargs['request']
            username = request['username']
            new_parent_dn = request['new_container']
            domain_dn = ldb.Dn(con, con.domain_dn())
            filter = ("(&(sAMAccountType=%d)(sAMAccountName=%s))" %
                  (dsdb.ATYPE_NORMAL_ACCOUNT, ldb.binary_encode(username)))
            res = con.search(base=domain_dn,
                               expression=filter,
                               scope=ldb.SCOPE_SUBTREE)
            user_dn = res[0].dn
            full_new_parent_dn = con.normalize_dn_in_domain(new_parent_dn)
            full_new_user_dn = ldb.Dn(con, str(user_dn))
            full_new_user_dn.remove_base_components(len(user_dn) - 1)
            full_new_user_dn.add_base(full_new_parent_dn)
            con.rename(user_dn, full_new_user_dn)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST, 'Unable to move group "%s"' % (e), None)
        return ResponseStatus(status.HTTP_200_OK, None, None)
    
        






class ResponseStatus:
	code=''
	description=''
	data = None
	def __init__(self,status,description,data):
		self.status = status
		self.data = data
		self.description=description