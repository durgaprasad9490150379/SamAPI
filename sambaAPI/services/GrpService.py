import sys
sys.path.insert(0, "/usr/local/samba/lib/python3.7/site-packages")


import samba
import ldb

from samba import dsdb
from samba.samdb import SamDB
from samba.param import LoadParm
from samba.auth import system_session
from samba.credentials import Credentials
from samba.ndr import ndr_unpack
from samba.dcerpc import security
from samba.dsdb import (
    ATYPE_SECURITY_GLOBAL_GROUP,
    GTYPE_SECURITY_BUILTIN_LOCAL_GROUP,
    GTYPE_SECURITY_DOMAIN_LOCAL_GROUP,
    GTYPE_SECURITY_GLOBAL_GROUP,
    GTYPE_SECURITY_UNIVERSAL_GROUP,
    GTYPE_DISTRIBUTION_DOMAIN_LOCAL_GROUP,
    GTYPE_DISTRIBUTION_GLOBAL_GROUP,
    GTYPE_DISTRIBUTION_UNIVERSAL_GROUP,
)

from rest_framework import status


class GrpService:
    connection_service = None

    def __init__(self, connection):
        self.connection_service = connection
    
    def list(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Invalid server details "%s": ' % (e), None)
        try:
            domain_dn = con.domain_dn()
            attrs=["*"]
            domain_dn = con.domain_dn()
            res = con.search(base=domain_dn, scope=ldb.SCOPE_SUBTREE, expression=("(objectClass=group)"), attrs=attrs)
#            domain_dn = con.domain_dn()
            if (len(res) == 0):
                return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found3: %s' % (e), None)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found: %s' % (e), None)
        return ResponseStatus(status.HTTP_200_OK,None,res)


    def list_members(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        try:
            groupname = kwargs['name']
            domain_dn = con.domain_dn()
            search_filter = "(&(objectClass=group)(samaccountname=%s))" % groupname
            res = con.search(domain_dn, scope=ldb.SCOPE_SUBTREE,expression=(search_filter),attrs=['*'])
            if (len(res) != 1):
                return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Group Not Found: %s' % (e), None)
            group_dn = res[0].get('dn', idx=0)
            object_sid = res[0].get('objectSid', idx=0)
            object_sid = ndr_unpack(security.dom_sid, object_sid)
            (group_dom_sid, rid) = object_sid.split()
            search_filter = "(|(primaryGroupID=%s)(memberOf=%s))" % (rid, group_dn)
            res = con.search(domain_dn, scope=ldb.SCOPE_SUBTREE,expression=(search_filter),attrs=['*'])
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found3: %s' % (e), None)
        return ResponseStatus(status.HTTP_200_OK,None,res)


    def create(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        try:
            request = kwargs['request']
            groupname = request['name']
            description = request['description']
            container = request['container']
#            group_type = request['group_type']
            notes = request['notes']
            mail_id = request['mail_id']
            res = con.newgroup(groupname=groupname, description=container, mailaddress=mail_id, notes=notes)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found3: %s' % (e), None)
        return ResponseStatus(status.HTTP_201_CREATED,None,res)

    def delete(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        try:
           # request = kwargs['request']
            groupname = kwargs['name']
            filter = ("(&(sAMAccountName=%s)(objectClass=group))" % (groupname))
            res = con.search(base=con.domain_dn(),scope=ldb.SCOPE_SUBTREE,expression=filter,attrs=['*'])
            if len(res)==0:
                return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found3', None)
            group_dn = res[0].dn
            print(res[0].dn)
            try:
                con.delete(group_dn)
            except Exception as e:
                return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Unable to delete group "%s"' % (e), None)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found1 "%s"' % (e), None)
        return ResponseStatus(status.HTTP_204_NO_CONTENT, 'Group deleted successfully',None)
    
    
    def add_members(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        try:
            request = kwargs['request']
            groupname = request['groupname']
            listofmembers = str(request['listofnames'])
            groupmembers = listofmembers.split(',')
            con.add_remove_group_members(groupname, groupmembers, add_members_operation=True)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Not Found "%s"' % (e), None)
        return ResponseStatus(status.HTTP_200_OK, 'success', None)

    def	remove_members(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s"' % (e), None)
        
        try:
            request = kwargs['request']
            groupname =	request['groupname']
            listofmembers = request['listofnames']
            remmembers = listofmembers.split(',')
            con.add_remove_group_members(groupname, remmembers,	add_members_operation=False)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST, 'Failed to remove members "%s" from group "%s"' %(remmembers, groupname), e)
        return ResponseStatus(status.HTTP_200_OK,"Removed members from group %s\n" % groupname,	None)

    def show(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invald server details "%s"' % (e), None)
        
        try:
            groupname = kwargs['name']
            filter = ("(&(sAMAccountType=%d)(sAMAccountName=%s))" %
                  (ATYPE_SECURITY_GLOBAL_GROUP,
                   ldb.binary_encode(groupname)))
            domaindn = con.domain_dn()
            res = con.search(base=domaindn, expression=filter,
                               scope=ldb.SCOPE_SUBTREE, attrs=['*'])
            user_dn = res[0].dn
            if (len(res) == 0):
                return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Group not found: "%s"' % (groupname), None)
            for msg in res:
                user_ldif = con.write_ldif(msg, ldb.CHANGETYPE_NONE)
                print(user_ldif)
        except Exception as e:
            return ResponseStatus(status.HTTP_400_BAD_REQUEST, 'Group Not found2: "%s"' % (e), None)
        return ResponseStatus(status.HTTP_200_OK, None, res)

class ResponseStatus:
    code=''
    description=''
    data = None
    def __init__(self,status,description,data):
        self.status = status
        self.data = data
        self.description=description

