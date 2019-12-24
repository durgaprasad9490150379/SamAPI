from rest_framework.test import APITestCase
from sambaAPI.domain.views import DomainViewSet
from rest_framework.test import APIRequestFactory

class TestDomainView(APITestCase):
	
	def setUp(self):
		self.factory = APIRequestFactory()

	def test_all_domain(self):
		request = self.factory.get('/domain/')
		response = DomainViewSet.as_view({'get':'list'})(request)
		response.render()
		self.assertEqual(response.status_code ,200,'Expected Response Code 200, received {0} instead.'.format(response.status_code))
		self.assertEqual(len(response.content), 2, 'expected response data length is 2 received {0} instead.'.format(len(response.content)))
	
	def test_domain(self):
		# create a new domain
	
		domain = {
			'domain_name': 'exza',
			'domain_controller': '192.168.100.164',
			'username': 'asmin',
			'password': 'admin'}
		request = self.factory.post('/domain/',data=domain)
		response = DomainViewSet.as_view({'post':'create'})(request)
		response.render()
		self.assertEqual(response.status_code,201,'Expected Response Code 201, received {0} instead.'.format(response.status_code))
		self.assertEqual(response.data,domain,'Should match domain data with response data. domain data is {0}'.format(domain)+' received response data is {0}.'.format(response.data))
	

		#update domain

		update_domain = {
			'domain_name': 'exza',
			'domain_controller': '192.168.100.131',
			'username': 'admin',
			'password': 'admin123'
		}

		update_request = self.factory.put('/domain/', data=update_domain)
		update_response = DomainViewSet.as_view({'put': 'update'})(update_request, pk='exza')
		self.assertEqual(update_response.status_code, 200, 'Expected response code is 200, received response code {0} instead.'.format(update_response.status_code))
		self.assertEqual(update_response.data,update_domain,'Should match domain data with response domain data.Expected domain data {0} '.format(update_domain)+ ' received data {0} instead'.format(update_response.data))
		

		#get domain by domain name

		get_request = self.factory.get('/domain/')
		get_response = DomainViewSet.as_view({'get':'retrieve'})(get_request,pk='exza')
		self.assertEqual(get_response.status_code,200,'Expected response code is 200, received response code {0} instead.'.format(get_response.status_code))
		self.assertEqual(get_response.data,update_domain,'Should match domain data with response domain data.Expected domain data {0} '.format(update_domain)+' received data {0} instead'.format(get_response.data))


		#delete domain

		delete_request = self.factory.delete('/domain/')
		delete_response = DomainViewSet.as_view({'delete':'destroy'})(delete_request,pk='exza')
		self.assertEqual(delete_response.status_code, 204,'Expected response code is 204, received response code {0} instead.'.format(delete_response.status_code))
