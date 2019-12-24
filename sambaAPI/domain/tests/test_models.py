from django.test import TestCase
from sambaAPI.domain.models import Domain

class TestDomainModels(TestCase):
	""" Test module for Domain model """

	def setUp(self):
		Domain.objects.create(
			domain_name='exza', domain_controller='192.168.100.164', username='admin', password='admin')


	def test_domain_model(self):
		domain_exza = Domain.objects.get(domain_name='exza')
		self.assertEqual(domain_exza.domain_name, "exza")
