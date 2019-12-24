import sys
from sambaAPI.services.OUService import OUService
import unittest
from unittest.mock import patch
from sambaAPI.services.OUService import ResponseStatus, OUService
from sambaAPI.orgunitmgt.models import OrgUnit

class MockConnectionService:
    domain = None
    def __init__(self,domain_name):
        try:
            self.domain = Domain()
            self.domain.domain_name = domain_name
        except Exception as e:
            self.domain = None
    
    def connection(self):
        con = MockConnection()
        return con

class MockConnection:
    def __init__(self):
        self.ou_data = []
        self.ou_data.append({'dn': 'OU=Tested123,DC=exza,DC=com',
                     'objectClass': [b'top', b'organizationalUnit'],
                     'description': [b'stringsssss'],
                     'instanceType': [b'4'],
                     'whenCreated': [b'20190620084756.0Z'],
                     'uSNCreated': [b'8289'],
                     'objectGUID': [b'\x020d\xbd\xc6\xad#E\x83\xcf\xc2\x07t\x112\x0c'],
                     'objectCategory': [b'CN=Organizational-Unit,CN=Schema,CN=Configuration,DC=exza,DC=com'],
                     'ou': [b'Tested123'],
                     'name': [b'Tested123'],
                     'whenChanged': [b'20190620094105.0Z'],
                     'uSNChanged': [b'8294'],
                     'distinguishedName': [b'OU=Tested,DC=exza,DC=com']})

        self.ou_data.append({'dn': 'OU=Tested123,DC=exza,DC=com',
                     'objectClass': [b'top', b'organizationalUnit'],
                     'description': [b'stringsssss'],
                     'instanceType': [b'4'],
                     'whenCreated': [b'20190620084756.0Z'],
                     'uSNCreated': [b'8289'],
                     'objectGUID': [b'\x020d\xbd\xc6\xad#E\x83\xcf\xc2\x07t\x112\x0c'],
                     'objectCategory': [b'CN=Organizational-Unit,CN=Schema,CN=Configuration,DC=exza,DC=com'],
                     'ou': [b'Tested123'],
                     'name': [b'Tested123'],
                     'whenChanged': [b'20190620094105.0Z'],
                     'uSNChanged': [b'8294'],
                     'distinguishedName': [b'OU=Tested,DC=exza,DC=com']})

        self.ou_data.append({'dn': 'OU=Tested111,DC=exza,DC=com',
                     'objectClass': [b'top', b'organizationalUnit'],
                     'description': [b'stringsssss'],
                     'instanceType': [b'4'],
                     'whenCreated': [b'20190620084756.0Z'],
                     'uSNCreated': [b'8289'],
                     'objectGUID': [b'\x020d\xbd\xc6\xad#E\x83\xcf\xc2\x07t\x112\x0c'],
                     'objectCategory': [b'CN=Organizational-Unit,CN=Schema,CN=Configuration,DC=exza,DC=com'],
                     'ou': [b'Tested111'],
                     'name': [b'Tested111'],
                     'whenChanged': [b'20190620094105.0Z'],
                     'uSNChanged': [b'8294'],
                     'distinguishedName': [b'OU=Tested,DC=exza,DC=com']})   

   
    def normalize_dn_in_domain(self,dn):
        if dn == "OU=":
            raise Exception("Empty Ou!!!!")
        elif dn is not None:
            if dn.startswith('OU='):
                return dn
            else:
                raise Exception("Enter valid OU")
        else:
            raise Exception("Enter valid Org unit")

    def search(self, **kwargs):
        res = []
        if kwargs['base'].startswith("OU="):
            temp = kwargs['base'][3:]
            temp = "[b'" + temp + "']"
        else:
            position = kwargs['expression'].rfind("name")
            sub_str = kwargs['expression'][position + 5:]
            sub_str = sub_str.translate({ord(')') : None})
            if(len(sub_str) != 0):
                temp = "[b'" + sub_str + "']"
            else:
                raise Exception("Enter valid ou!!!")
        counter = 0
        for d in self.ou_data:
            temp2 = d.get('name')
            if str(temp) == str(temp2):
                res.append(d)
                counter = counter + 1
        if counter > 1:
           raise Exception("Exception ocured!!")
        return res


    def create_ou(self, ou_dn, **kwargs):
        if ou_dn != '':
            if ou_dn is not None:
                for d in self.ou_data:
                    base = ou_dn
                    name = d.get('name')
                    base = "b'"+ (base[3:])+"'"
                    if str(base) == str(name[0]):
                        raise Exception('Organization unit already exist with name')
            else:
                raise Exception('Organization unit is not valid')
        else:
            raise Exception('Organization unit is not valid')

    def delete_ou(self,dname,controls):
        x = dname[0]
        if dname != '':
            if dname is not None:
                for d in self.ou_data:
                    if x.get('name') == d.get('name'):
                        return None
        raise Exception("Exception occured!!!")

    def rename(self, full_old_ou_dn, full_new_ou_dn):
        if full_new_ou_dn is not None:
            if full_new_ou_dn != '':
                for d in self.ou_data:
                    name = d.get('dn')
                    if  str(name) == str(full_old_ou_dn):
                        raise Exception('Organization name already exist with name')
                    else:
                        return None
            else:
                raise Exception('Organization name is not valid')
        else:
            raise Exception('Organization name is not valid')

        
    def domain_dn(self):
        return 'dc=exza,dc=com'


class TestService(unittest.TestCase):
    def setUp(self):
        self.connection=MockConnectionService('exza')
        
    def test_list(self):
        res = OUService(self.connection).list()
        self.assertEqual(res.status,200)

    def test_create(self):
        data = {'name': 'testou', 'description': 'testing ou', 'domain_name': 'DC=exza,DC=com'}
        ou = OrgUnit()
        ou.name = data['name']
        ou.description = data['description']
        response = OUService(self.connection).create(ou=ou,request=data)
        self.assertEqual(response.status,201)

    def test_same_name_create(self):
        data = {'name': 'Tested123', 'description': 'testing ou', 'domain_name': 'DC=exza,DC=com'}
        ou = OrgUnit()
        ou.name = data['name']
        ou.description = data['description']
        response = OUService(self.connection).create(ou=ou,request=data)
        self.assertEqual(response.status,400)

    def test_delete_valid(self):
        data = {'name' : 'Tested111'}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).delete(ou=ou,force_subtree_delete=False)
        self.assertEqual(response.status, 204)


    def test_delete_empty(self):
        data = {'name': ''}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).delete(ou=ou, force_subtree_delete=False)
        self.assertEqual(response.status, 400)


    def test_delete_wrong(self):
        data = {'name': 'aaaaaa'}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).delete(ou=ou, force_subtree_delete=False)
        self.assertEqual(response.status, 404)

    def test_delete_repeated(self):
        data = {'name': 'Tested123'}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).delete(ou=ou, force_subtree_delete=False)
        self.assertEqual(response.status, 409)

    def test_edit_valid(self):
        data = {'name' : 'Tested111'}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).edit(name=ou.name)
        self.assertEqual(response.status, 200)
  
    def test_edit_wrong(self):
        data = {'name' : '111'}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).edit(name=ou.name)
        self.assertEqual(response.status, 404)

    def test_edit_repeated(self):
        data = {'name' : 'Tested123'}
        ou = OrgUnit()
        ou.name = data['name']
        response = OUService(self.connection).edit(name=ou.name)
        self.assertEqual(response.status, 409)

    def test_edit_conflict(self):
        name = 'Tested123'
        response = OUService(self.connection).edit(name=name)
        self.assertEqual(response.status, 409)

    def test_edit(self):
        name = 'Tested111'
        response = OUService(self.connection).edit(name=name)
        self.assertEqual(response.status, 200)

    def test_empty_name_create(self):
        invalid_data = {'name':'', 'description': 'testing ou', 'domain_name': 'DC=exza,DC=com'}
        ou = OrgUnit()
        ou.name = invalid_data['name']
        ou.description = invalid_data['description']
        response = OUService(self.connection).create(ou=ou,request = invalid_data)
        self.assertEqual(response.status, 400)

    
    # def test_connection_create(self):
        # data = {'name': 'testou', 'description': 'testing ou', 'domain_name': 'DC=exza,DC=com'}
        # ou = OrgUnit()
        # ou.name = data['name']
        # ou.description = data['description']
        # response = OUService(self.connection1).create(ou=ou,request=data)
        # self.assertEqual(response.status,500)

        
    def test_invalid_rename(self):
        data = {'name':'Testing12345'}
        old_name = 'Tested'
        response = OUService(self.connection).rename(old_name = old_name, request = data)
        self.assertEqual(response.status, 404) 

    def test_valid_rename_conflict(self):
        data = {'name':'Testing1234'}
        old_name = 'Tested123'
        response = OUService(self.connection).rename(old_name=old_name,request=data)
        self.assertEqual(response.status,409)

    def test_valid_rename(self):
        data = {'name':'ExzaTech'}
        old_name = 'Tested111'
        print(data)
        response = OUService(self.connection).rename(old_name=old_name,request=data)
        print(response.description)
        self.assertEqual(response.status,200)

    
    def test_empty_new_name_rename(self):
        data = {'name': ''}
        old_name = 'Tested123'
        response = OUService(self.connection).rename(old_name = old_name, request = data)
        self.assertEqual(response.status, 400) 

    def test_empty_old_name_rename(self):
        data = {'name': 'Testing1234'}
        old_name = ''
        response = OUService(self.connection).rename(old_name = old_name, request = data)
        self.assertEqual(response.status,400)
   
    def test_same_name_rename(self):
        data = {'name': 'Tested123'}
        old_name = 'Tested123'
        response = OUService(self.connection).rename(old_name = old_name, request = data)
        self.assertEqual(response.status,409)
    

