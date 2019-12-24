import json
from sambaAPI.domain.views import DomainViewSet
from rest_framework.test import APIRequestFactory
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from sambaAPI.domain.models import Domain
from sambaAPI.domain.serializers import DomainSerializer
from rest_framework import status
from django.test import TestCase, Client

client = Client()


class TestDomainView(TestCase):

    def setUp(self):

        self.factory = APIRequestFactory()

        Domain.objects.create(
           domain_name='exzatech', domain_controller='198.0.0.126', username='admin', password='admin@123')

        self.muffin = Domain.objects.create(
            domain_name='testing', domain_controller='198.100.100.197', username='admined', password='admin@123')
        
        self.valid_payload = {
            'domain_name': 'exza',
            'domain_controller': '198.168.0.9',
            'username': 'testing',
            'password': 'tested'
        }
        self.invalid_payload = {
            'domain_name': '',
            'domain_controller': 4,
            'username': 'Pamerion',
            'password': 'White'
        }
        
        self.update_payload = {
            'domain_name': 'exzatech',
            'domain_controller': '198.0.0.126',
            'username': 'admin',
            'password': 'admin@123'
        }

    # Get domain list

    def test_get_all_domains(self):
       response = client.get('/domain/')
       domain = Domain.objects.all()
       serializer = DomainSerializer(domain, many=True)
       self.assertEqual(response.data, serializer.data) 
       self.assertEqual(response.status_code ,200,'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    # get domian by domain name

    
    def test_get_valid_single_domain(self):
        get_request = self.factory.get('/domain/')
        get_response = DomainViewSet.as_view({'get':'retrieve'})(get_request,pk='exzatech')
        self.assertEqual(get_response.status_code,200,'Expected response code is 200, received response code {0} instead.'.format(get_response.status_code))
        self.assertEqual(get_response.data,self.update_payload,'Should match domain data with response domain data.Expected domain data {0} '.format(self.update_payload)+' received data {0} instead'.format(get_response.data)) 

    def test_get_invalid_single_domain(self):
        get_request = self.factory.get('/domain/')
        get_response = DomainViewSet.as_view({'get':'retrieve'})(get_request,pk='exza')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    # create a new domain

    def test_create_valid_domain(self):
        request = self.factory.post('/domain/',data=self.valid_payload)
        response = DomainViewSet.as_view({'post':'create'})(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code,201,'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        self.assertEqual(response.data,self.valid_payload,'Should match domain data with response data. domain data is {0}'.format(self.valid_payload)+' received response data is {0}.'.format(response.data))

    def test_create_invalid_domain(self):
       response = client.post('/domain/', data=self.invalid_payload)
       self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       

    # update domain

    def test_valid_update_domain(self):
        update_request = self.factory.put('/domain/', data=self.update_payload)
        update_response = DomainViewSet.as_view({'put': 'update'})(update_request, pk='exzatech')
        self.assertEqual(update_response.status_code, 200, 'Expected response code is 200, received response code {0} instead.'.format(update_response.status_code))
        self.assertEqual(update_response.data,self.update_payload,'Should match self.update_payload data with response domain data.Expected domain data {0} '.format(self.update_payload)+ ' received data {0} instead'.format(update_response.data))

    def test_invalid_update_domain(self):
        update_request = self.factory.put('/domain/', data=self.invalid_payload)
        update_response = DomainViewSet.as_view({'put': 'update'})(update_request, pk='exzatech')
        self.assertEqual(update_response.status_code, status.HTTP_400_BAD_REQUEST)


    #delete domain

    def test_valid_delete_domain(self):
        delete_request = self.factory.delete('/domain/')
        delete_response = DomainViewSet.as_view({'delete':'destroy'})(delete_request,pk='exzatech')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertEqual(delete_response.data,self.update_payload,'Should match domain data with response domain data.Expected domain data {0} '.format(self.update_payload)+ ' received data {0} instead'.format(delete_response.data))   

    def test_invalid_delete_domain(self):
        delete_request = self.factory.delete('/domain/')
        delete_response = DomainViewSet.as_view({'delete':'destroy'})(delete_request,pk='test1')
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)

