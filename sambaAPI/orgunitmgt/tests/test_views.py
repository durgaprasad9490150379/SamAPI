from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from sambaAPI.orgunitmgt import views
from sambaAPI.services.OUService import ResponseStatus
from rest_framework import status

class TestOrgUnitView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('sambaAPI.orgunitmgt.views.OUService.create')
    def test_mock_create(self, mock_OUService_create):
        valid_ou={
            'name': 'Testing',
            'description': 'Testing API',
            'domain_name': 'OU=PY,DC=exza,DC=com'
        }
        mock_OUService_create.return_value = ResponseStatus(status.HTTP_201_CREATED, valid_ou, None)
        request = self.factory.post('/ou/create/', data=valid_ou)
        response = views.create(request)
        self.assertEqual(response.status_code, 201,
                              'Expected Response Code 201, received {0} instead.'.format(response.status_code))
        self.assertEqual(response.data,valid_ou)


    @patch('sambaAPI.orgunitmgt.views.OUService.create')
    def test_mock_create_invalid(self, mock_OUService_create):
        invalid_ou = {
            'name': '',
            'description': '',
            'domain_name': ''
        }
        mock_OUService_create.return_value = ResponseStatus(status.HTTP_400_BAD_REQUEST,'Invalid old_ou_dn',None)

        request = self.factory.post('/ou/create/', data={})
        response = views.create(request)
        self.assertEqual(response.status_code, 400,
                       'Expected Response Code 400, received {0} instead.'.format(response.status_code))




    @patch('sambaAPI.orgunitmgt.views.OUService.delete')
    def test_delete_valid(self, mock_OUService_delete):
        name = "Durga"
        mock_OUService_delete.return_value = ResponseStatus(status.HTTP_204_NO_CONTENT, 'OU deleted successfully', None)
        request = self.factory.delete('/ou/delete')
        response = views.delete(request, name)
        self.assertEqual(response.status_code, 204,
                         'Expected Response code 204, received {0} instaed.'
                         .format(response.status_code))



    @patch('sambaAPI.orgunitmgt.views.OUService.delete')
    def test_delete_invalid(self, mock_OUService_delete):
        mock_OUService_delete.return_value = ResponseStatus(status.HTTP_409_CONFLICT, 'Failed to delete ou',None)
        name = ""
        request = self.factory.delete('/ou/delete')
        response = views.delete(request, name)
        self.assertEqual(response.status_code,409,
                         'Expected Response code 409, received {0} instead.'.format(response.status_code))
   
     



    @patch('sambaAPI.orgunitmgt.views.OUService.rename')
    def test_rename_valid(self, mock_OUService_rename):
        old_name = "Durga"
        new_name = "Prasad"
        mock_OUService_rename.return_value = ResponseStatus(status.HTTP_200_OK, '%s renamed successfully' % old_name, None)
        request = self.factory.put('/ou/rename/', new_name)
        response = views.rename(request, old_name)
        self.assertEqual(response.status_code, 200,
                         'Expected Response code 200, received {0} instead.'.format(response.status_code))


    @patch('sambaAPI.orgunitmgt.views.OUService.rename')
    def test_rename_invalid(self, mock_OUService_rename):
        old_name = ""
        new_name = "Prasad"
        mock_OUService_rename.return_value = ResponseStatus(status.HTTP_409_CONFLICT, 'OU is invalid ', None)
        request = self.factory.put('/ou/rename/', new_name)
        response = views.rename(request, old_name)
        self.assertEqual(response.status_code, 409,
                         'Expected Response code 409, received {0} instead.'.format(response.status_code))




    @patch('sambaAPI.orgunitmgt.views.OUService.edit')
    def test_edit_valid(self, mock_OUService_edit):
        ou_name = "Durga"
        mock_OUService_edit.return_value = ResponseStatus(status.HTTP_200_OK, ou_name, None)
        request = self.factory.get('/ou/edit/')
        response = views.edit(request, ou_name)
        self.assertEqual(response.status_code, 200,
                              'Expected Response Code 200, received {0} instead.'.format(response.status_code))



    @patch('sambaAPI.orgunitmgt.views.OUService.edit')
    def test_edit_invalid(self, mock_OUService_edit):
        ou_name = ""
        mock_OUService_edit.return_value = ResponseStatus(status.HTTP_200_OK, ou_name, None)
        request = self.factory.get('/ou/edit/')
        response = views.edit(request, ou_name)
        self.assertEqual(response.status_code, 200,
                              'Expected Response Code 200, received {0} instead.'.format(response.status_code))

