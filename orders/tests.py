from django.test import TestCase

# Create your tests here.
import json
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth.models import User

from .models import Order, OrderDetail
from products.models import Product

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

    def create_example_products(self):
        for value in range(0, 10):
            test_product = {
                "id": f"z00{value}",
                "name": f"test {value}",
                "price": 10,
                "stock": 10
            }
            temp = Product.objects.create(**test_product)

    def create_example_order(self):
        test_order = Order.objects.create()
        for item in range(0, 4):
            order_item = {
                'order': test_order,
                'product_id': f'z00{item}',
                'quantity': 1,
            }
            test_order_item = OrderDetail.objects.create(**order_item)
        return test_order

    def test_create_order(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.create_example_products()

        test_order = {
            "date_time": "2022-02-09T03:12:16.925445Z",
            "items": [
                {
                    "quantity": 2,
                    "product": "z001"
                },
                {
                    "quantity": 4,
                    "product": "z002"
                },
                {
                    "quantity": 3,
                    "product": "z003"
                }
            ]
        }

        response = client.post(
            '/order/',
            test_order,
            format='json'
        )
        result = json.loads(response.content)
        product_z001 = Product.objects.get(id='z001')
        product_z002 = Product.objects.get(id='z002')
        product_z003 = Product.objects.get(id='z003')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg='Orden Creadad correctamente')
        self.assertEqual(result.get('get_total'), 90, msg='el total de la orden es correcto')
        self.assertIsNotNone(result.get('get_total_usd'), msg='Existe cotizacion en dolares')

        self.assertEqual(product_z001.stock, 8, msg='test nuevo stock producto z001')
        self.assertEqual(product_z002.stock, 6, msg='test nuevo stock producto z002')
        self.assertEqual(product_z003.stock, 7, msg='test nuevo stock producto z003')

    def test_delete_order(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.create_example_products()

        test_order = self.create_example_order()

        response = client.delete(
            f'/order/{test_order.id}/',
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg='Test eliminar Order')

        product_z000 = Product.objects.get(id='z000')
        product_z001 = Product.objects.get(id='z001')
        product_z002 = Product.objects.get(id='z002')
        product_z003 = Product.objects.get(id='z003')

        self.assertEqual(product_z000.stock, 10, 'Test stock producto restablecido')
        self.assertEqual(product_z001.stock, 10, 'Test stock producto restablecido')
        self.assertEqual(product_z002.stock, 10, 'Test stock producto restablecido')
        self.assertEqual(product_z003.stock, 10, 'Test stock producto restablecido')

    def test_update_order(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.create_example_products()

        test_order = self.create_example_order()
        new_data_order = {
            "date_time": "2022-02-09T03:12:16.925445Z",
            "items": [
                {
                    "quantity": 2,
                    "product": "z000"
                },

                {
                    "quantity": 2,
                    "product": "z001"
                },

            ]
        }

        response = client.put(
            f'/order/{test_order.id}/',
            new_data_order,
            format='json'
        )
        result = json.loads(response.content)
        expected_item_result = [{'id': 1, 'order': 1, 'quantity': 2, 'product': 'z000'}, {'id': 2, 'order': 1, 'quantity': 2, 'product': 'z001'}]
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Actualizado correctamente')
        self.assertEqual(result.get('items'), expected_item_result, msg='Valores correctamente actualizados')

    def test_listar_orders(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.create_example_products()

        test_order = self.create_example_order()
        test_order = self.create_example_order()

        response = client.get(
            f'/order/',
            format='json'
        )
        result = json.loads(response.content)
        total_listed = result.get('count')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg='Lsitado correctamente')
        self.assertEqual(total_listed, 2, msg='Cantidad listada correctamente')


