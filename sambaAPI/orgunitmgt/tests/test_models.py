import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestOrgUnit:
    def test_model(self):
        obj = mixer.blend('orgunitmgt.OrgUnit',name='Testing',description='Testing API',domain_name='OU=PY,DC=exza,DC=com')
        assert obj.name == 'Testing', 'Should create a OrgUnit instance'