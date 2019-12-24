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

class CMServices:
    connection_service = None

    def __init__(self, connection):
        self.connection_service = connection
    
    def list(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        domain_dn = con.domain_dn()
        res = con.search(expression="(objectClass= computer)", scope=ldb.SCOPE_SUBTREE, attrs=[])
        if(len(res) == 0):
            return ResponseStatus(status.HTTP_404_NOT_FOUND,None,None)
        print(str(res))
        return ResponseStatus(status.HTTP_200_OK,None,res)

    def create(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        cm = kwargs['cm']
        request = kwargs['request']
        try:
            con.newcomputer(cm.computer_name, cm.domain_container, cm.description)
        except Exception as e:
           print(str(e))
           return ResponseStatus(status.HTTP_400_BAD_REQUEST,'Failed to create computer "%s": %s' % (request['computer_name'], e),None)
        print(request['computer_name'], request['description'])
        return ResponseStatus(status.HTTP_201_CREATED,request['computer_name'],None)


    def delete(self, **kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        samaccountname = kwargs['computer_name'] + "$"
        print(samaccountname)
        exp = ("(&(sAMAccountType=%d)(sAMAccountName=%s))" %
                  (dsdb.ATYPE_WORKSTATION_TRUST,
                   ldb.binary_encode(samaccountname)))
        domain_dn = con.domain_dn()

        try:
            res = con.search(base=domain_dn, scope=ldb.SCOPE_SUBTREE, expression=exp, attrs=[])
            print(str(res))
            if len(res) == 0:
                return ResponseStatus(status.HTTP_404_NOT_FOUND,'Unable to find computer  "%s"\n' % computer_name,None)
           
            computer_dn = res[0].dn
            print("comp_dn: " + str(computer_dn))
            computer_ac = int(res[0]["userAccountControl"][0])
            if "dNSHostName" in res[0]:
                computer_dns_host_name = str(res[0]["dNSHostName"][0])
            else:
                computer_dns_host_name = None
        except Exception as e:
            return ResponseStatus(status.HTTP_404_NOT_FOUND,'Unable to find computer  "%s"\n' % samaccountname,None)
        
        computer_is_workstation = (computer_ac & dsdb.UF_WORKSTATION_TRUST_ACCOUNT)
        if not computer_is_workstation:
            print("Computer is not a workstation")
            return ResponseStatus(status.HTTP_409_CONFLICT, 'Failed to remove computer "%s": ' % samaccountname)
        
        try:
            con.delete(computer_dn)
            if computer_dns_host_name:
                remove_dns_references(con, self.get_logger(), computer_dns_host_name, ignore_no_name=True)
        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT, 'Failed to delete computer "%s": %s' % (samaccountname, e),None)
        return ResponseStatus(status.HTTP_204_NO_CONTENT,None, None)



    def show(self,**kwargs):
        try:
            con = self.connection_service.connection()
        
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)
        
        samaccountname = kwargs['computer_name'] + "$"
        print("ser: " + samaccountname)     
        #domain_dn = ldb.Dn(con, con.domain_dn())
        domain_dn = con.domain_dn()
        exp = ("(&(sAMAccountType=%d)(sAMAccountName=%s))" %
                  (dsdb.ATYPE_WORKSTATION_TRUST,
                   ldb.binary_encode(samaccountname)))
        try:
            res = con.search(base=domain_dn, scope=ldb.SCOPE_SUBTREE, expression=exp, attrs=['*'])
            print("Response from Samba")
            for i in range(0, len(res)):
                r = str(res[i]['name'])
                print("comp_name: " + r)
                s = str(res[i]['description'])
                print("desc: " + s)
                c = str(res[i]['dn'])
                print("dn: " + c)
            if len(res) == 0:
                return ResponseStatus(status.HTTP_404_NOT_FOUND,None,None) 
        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT,None,None)
        return ResponseStatus(status.HTTP_200_OK, None, res)




    def rename(self,**kwargs):
        try:
            con = self.connection_service.connection()
        except Exception as e:
            return ResponseStatus(status.HTTP_500_INTERNAL_SERVER_ERROR,'Invalid server details "%s": ' % (e),None)

        # request = kwargs['request']
        samaccountname = kwargs['computer_name'] + "$"
        new_ou_dn = kwargs['domain_container']

        domain_dn = ldb.Dn(con, con.domain_dn())
        
        exp = ("(&(sAMAccountType=%d)(sAMAccountName=%s))" %
                  (dsdb.ATYPE_WORKSTATION_TRUST,
                   ldb.binary_encode(samaccountname)))
	
        try:
            res = con.search(base=domain_dn, expression= exp, scope=ldb.SCOPE_SUBTREE)
            if len(res) == 0:
                return ResponseStatus(status.HTTP_404_NOT_FOUND,'Unable to find computer "%s"\n' % kwargs['computer_name'], None)
            computer_dn = res[0].dn
            print("Computer_dn" + str(computer_dn))
            full_new_ou_dn = ldb.Dn(con, new_ou_dn)
            if not full_new_ou_dn.is_child_of(domain_dn):
                full_new_ou_dn.add_base(domain_dn)
            new_computer_dn = ldb.Dn(con, str(computer_dn))
            new_computer_dn.remove_base_components(len(computer_dn) -1)
            new_computer_dn.add_base(full_new_ou_dn)
            con.rename(computer_dn, new_computer_dn)

        except Exception as e:
            return ResponseStatus(status.HTTP_409_CONFLICT,'Failed to rename ou "%s": %s' % (new_ou_dn, e),None)
        return ResponseStatus(status.HTTP_200_OK, request, None)






        
class ResponseStatus:
	code=''
	description=''
	data = None
	def __init__(self,status,description,data):
		self.status = status
		self.data = data
		self.description=description

