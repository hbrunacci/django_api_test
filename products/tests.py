from django.test import TestCase

# Create your tests here.
import json
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth.models import User

from .models import Product

class ProductTestCase(TestCase):

    def setUp(self):
        user = User(
            username='test_admin',
            email='test_admin@admin.com',
            first_name='Admin',
            last_name='Test',

        )
        user.set_password('admin123')
        user.save()

        client = APIClient()
        response = client.post(
                '/api/token/', {
                'username':'test_admin',
                'password': 'admin123',
            },
            format='json'
        )

        result = json.loads(response.content)
        self.access_token = result['access']
        self.refresh_token = result['refresh']
        self.user = user

    def test_create_product(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_product = {
            "id": "z001",
            "name": "test 1",
            "price": 60.50,
            "stock": 10
        }
        response = client.post(
            '/product/',
            test_product,
            format='json'
        )
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result, test_product)

        response = client.post(
            '/product/',
            test_product,
            format='json'
        )
        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['id'], ["product with this id already exists."])

    def test_delete_product(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_product = {
            "id": "z001",
            "name": "test 1",
            "price": 60.50,
            "stock": 10
        }
        temp_product = Product.objects.create(**test_product)

        response = client.delete(
            f'/product/{temp_product.id}/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_full_update_product(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_product = {
            "id": "z001",
            "name": "test 1",
            "price": 60.50,
            "stock": 10
        }
        new_data_test_product = {
            "id": "z001",
            "name": "test 2",
            "price": 50.00,
            "stock": 5
        }

        temp_product = Product.objects.create(**test_product)

        response = client.put(
            f'/product/{temp_product.id}/',
            new_data_test_product,
            format='json'
        )

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data_test_product, result)

    def test_partial_update_product(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        test_product = {
            "id": "z001",
            "name": "test 1",
            "price": 60.50,
            "stock": 10
        }
        new_data_test_product = {
            "stock": 5
        }

        temp_product = Product.objects.create(**test_product)

        response = client.patch(
            f'/product/{temp_product.id}/',
            new_data_test_product,
            format='json'
        )
        test_product['stock'] = 5

        result = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_product, result)
        temp_product = Product.objects.get(id='z001')
        self.assertEqual(temp_product.stock, 5)

    def test_list_products(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        for value in range(0, 10):
            test_product = {
                "id": f"z00{value}",
                "name": f"test {value}",
                "price": 10,
                "stock": 10
            }
            temp = Product.objects.create(**test_product)

        response = client.get(
            f'/product/',
            format='json'
        )

        result = json.loads(response.content)
        total_listed = result.get('count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(total_listed, 10)





