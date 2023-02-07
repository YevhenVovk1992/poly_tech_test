from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, APIClient

from event_manager import views, models


# Create your tests here.
class AddEventTestCase(APITestCase):
    class UserMock:
        """
        Mock for the user. Using in access check
        """

        def is_authenticated(self, *args, **kwargs):
            return True

        def is_active(self, *args, **kwargs):
            return True

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.data = {"event_type": "Sleep", "info": {"all_info": "text"}, "timestamp": "2023-09-06 17:45:05"}
        self.url = reverse('create_event')
        self.user = User.objects.create(
            username='Test',
            password='test12345-',
            email='test@test.com',
            first_name='usertest',
            last_name='last_name_test'
        )
        self.user.save()
        self.token = Token.objects.create(
            key='838ee6f374fa04bce8dc910217fb18dd4f8e2f7b',
            created='2023-02-06 13:23:55.161029',
            user_id='1'
        )
        self.token.save()

    def tearDown(self) -> None:
        pass

    def test_api_get_method_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertTrue('Authentication credentials were not provided.' in response.data['detail'])

    def test_api_get_method_with_user_auth(self):
        user = self.UserMock()
        view = views.EventViewSets.as_view({'post': 'create'})
        request = self.factory.get(self.url)
        request.user = user
        response = view(request)
        self.assertEqual(response.status_code, 405)
        self.assertTrue('Method "GET" not allowed.' in response.data['detail'])

    def test_api_with_anonymous_user(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(models.Event.objects.count(), 0)
        self.assertTrue('Authentication credentials were not provided.' in response.data['detail'])

    def test_api_with_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Event.objects.count(), 1)
        self.assertEqual(models.Event.objects.get().info, {"all_info": "text"})

    def test_id_model_and_pk_model(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Event.objects.get().pk, 1)
        self.assertEqual(str(type(models.Event.objects.get().id)), "<class 'uuid.UUID'>")
        self.assertEqual(len(str(models.Event.objects.get().id)), 36)

    def test_api_with_empty_data(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(models.Event.objects.count(), 0)
        self.assertTrue('Bad Request' in response.reason_phrase)

    def test_api_with_invalid_timestamp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {"event_type": "Sleep", "info": {"all_info": "text"}, "timestamp": "1992-09-06 17:45:05"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Date must not be in past time' in response.data['timestamp'][0])
        self.assertTrue('Bad Request' in response.reason_phrase)

    def test_api_with_invalid_event_type(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {"event_type": "", "info": {"all_info": "text"}, "timestamp": "2066-09-06 17:45:05"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('This field may not be blank.' in response.data['name'][0])
        self.assertTrue('Bad Request' in response.reason_phrase)

    def test_api_with_invalid_json_key(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {"event_type": "Run", "info": {"all_info": "text"}, "timestamp": "2066-09-06 17:45:05", "test": "test"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Event.objects.count(), 1)

    def test_with_wrong_token(self):
        token = '838ee6f374fa04bce8dc910217fb18dd4f8e2111'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, 401)


class AccountTestCase(APITestCase):
    def test_create_user(self):
        url = reverse('register_user')
        data = {'username': 'Test',
                'password': 'test12345-',
                'password2': 'test12345-',
                'email': 'test@test.com',
                'first_name': 'usertest',
                'last_name': 'last_name_test'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'Test')

    def test_create_user_short_password(self):
        url = reverse('register_user')
        data = {'username': 'Test',
                'password': 'test',
                'password2': 'test',
                'email': 'test@test.com',
                'first_name': 'usertest',
                'last_name': 'last_name_test'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_create_user_wrong_password2(self):
        url = reverse('register_user')
        data = {'username': 'Test',
                'password': 'test',
                'password2': 'test2',
                'email': 'test@test.com',
                'first_name': 'usertest',
                'last_name': 'last_name_test'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)


class TokenTestCase(APITestCase):
    pass