import sys
sys.path.insert(0, "/usr/local/samba/lib/python3.7/site-packages")


import samba
import ldb

from samba import dsdb
from samba.samdb import SamDB
from samba.param import LoadParm
from samba.auth import system_session
from samba.credentials import Credentials
from rest_framework import status

class OUService:
	connection_service = None

	def __init__(self, connection):
		self.connection_service = connection

	def list(self,**kwargs):
		try:
			con = self.connection_service.connection()
		except Exception as e:
			return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
		res = con.search(base=con.domain_dn(), scope=ldb.SCOPE_SUBTREE, expression="(objectClass=organizationalUnit)", attrs=[])
		return ResponseStatus(status.HTTP_200_OK,None,res)

	def create(self, **kwargs):
                try:
                        con = self.connection_service.connection()
                except Exception as e:
                        return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

                ou = kwargs['ou']
                try:
                        full_ou_dn = con.normalize_dn_in_domain("OU=%s" % ou.name)
                except Exception as e:
                        return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Invalid ou_dn "%s": %s' % (ou, e),None)

                try:
                        con.create_ou(full_ou_dn, description=ou.description)
                except Exception as e:
                        return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Failed to create ou "%s": %s' % (full_ou_dn, e),None)

                return ResponseStatus(status.HTTP_201_CREATED,kwargs['request'],None)

	def delete(self, **kwargs):
                try:
                        con = self.connection_service.connection()
                except Exception as e:
                        return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

                ou = kwargs['ou']
                try:
                        full_ou_dn = con.normalize_dn_in_domain("OU=%s" % ou.name)
                except Exception as e:
                        return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Invalid ou_dn "%s": %s' % (ou, e),None)

                controls = []
                force_subtree_delete = kwargs['force_subtree_delete']
                if force_subtree_delete:
                        controls = ["tree_delete:1"]
                try:
                        res = con.search(base=full_ou_dn, expression="(objectclass=organizationalUnit)", scope=ldb.SCOPE_BASE,attrs=[])
                        print("result:")
                        print(res['name'])
                        if len(res) == 0:
                                return ResponseStatus(status.HTTP_404_NOT_FOUND,'Unable to find ou "%s"\n' % ou,None)
                        con.delete_ou(res, controls)
                except Exception as e:
                        return ResponseStatus(status.HTTP_409_CONFLICT, 'Failed to delete ou "%s": %s' % (full_ou_dn, e),None)
                return ResponseStatus(status.HTTP_204_NO_CONTENT, 'Organizational Unit deleted successfully',None)

	def rename(self,**kwargs):
		try:
			con = self.connection_service.connection()
		except Exception as e:
			return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

		request = kwargs['request']
		try:
			full_old_ou_dn = con.normalize_dn_in_domain("OU=%s" % kwargs['old_name'])
		except Exception as e:
			return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Invalid old_ou_dn "%s": %s' % (kwargs['old_name'], e),None)
		try:
			full_new_ou_dn = con.normalize_dn_in_domain("OU=%s" % request['name'])
		except Exception as e:
			return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Invalid new_ou_dn "%s": %s' % (request['name'], e),None)
		
		try:
			res = con.search(base=full_old_ou_dn, expression="(objectclass=organizationalUnit)", scope=ldb.SCOPE_BASE,
							 attrs=["*"])
			if len(res) == 0:
				return ResponseStatus(status.HTTP_404_NOT_FOUND,'Unable to find ou "%s"\n' % kwargs['old_name'],None)
			con.rename(full_old_ou_dn, full_new_ou_dn)
		except Exception as e:
			return ResponseStatus(status.HTTP_409_CONFLICT,'Failed to rename ou "%s": %s' % (full_old_ou_dn, e),None)

		return ResponseStatus(status.HTTP_200_OK,request,None)

	def edit(self,**kwargs):
                try:
                        con = self.connection_service.connection()
                except Exception as e:
                        return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
               #domain_dn = ldb.Dn(con, con.domain_dn())
                domain_dn = con.domain_dn()
                exp = "(&(objectClass=organizationalUnit)(name=" + kwargs['name'] + "))"
                print("name:")
                print(kwargs['name'])
                print("exp:")
                print(exp)
               #full_new_ou_dn = con.normalize_dn_in_domain("OU=%s" % request['name'])
		
                try:
                        res = con.search(base=domain_dn, scope=ldb.SCOPE_SUBTREE, expression=exp, attrs=['*'])
                        for i in range(0, len(res)):
                            r = str(res[i]['dn'])
                            print(r)
                            s = str(res[i]['description'])
                            print(s)
                        print("result")
                        print(res)
                        if len(res) == 0:
	                            return ResponseStatus(status.HTTP_404_NOT_FOUND,None,None) 
			
                except Exception as e:
                        return ResponseStatus(status.HTTP_409_CONFLICT,None,None)
                return ResponseStatus(status.HTTP_200_OK, None, None)





class ResponseStatus:
	code=''
	description=''
	data = None
	def __init__(self,status,description,data):
		self.status = status
		self.data = data
		self.description=description
