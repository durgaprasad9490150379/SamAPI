from sambaAPI.domain.models import Domain
import factory

class DomainFactory(factory.Factory):
        class Meta:
            model = Domain

        domain_name = factory.Faker('exza')
        domain_controller = factory.Faker('192.168.100.26')
        username = factory.Faker('Admin')
        password = factory.Faker('Test@123')