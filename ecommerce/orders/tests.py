from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Product
from orders.models import Cart, CartItem, Order, OrderItem


class EcommerceAPITests(APITestCase):

    def setUp(self):
        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product',
            price=19.99,
            stock=10
        )

    def test_complete_ecommerce_flow(self):
        # 1. Register User
        register_url = reverse('register')
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(register_url, register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

        # 2. Token Auth (Login)
        token_url = reverse('token_obtain_pair')
        login_data = {
            'username': 'newuser',
            'password': 'newpassword123'
        }
        response = self.client.post(token_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        access_token = response.data['access']

        # Set Authorization Header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # 3. Browse Products
        products_url = reverse('product-list')
        response = self.client.get(products_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Product')

        # 4. View Empty Cart
        cart_url = reverse('cart')
        response = self.client.get(cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)

        # 5. Add to Cart
        cart_data = {
            'product': self.product.id,
            'quantity': 2
        }
        response = self.client.post(cart_url, cart_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product'], self.product.id)
        self.assertEqual(response.data['items'][0]['quantity'], 2)

        # 6. Increment Quantity (post again)
        cart_data_increment = {
            'product': self.product.id,
            'quantity': 3
        }
        response = self.client.post(cart_url, cart_data_increment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['items'][0]['quantity'], 5)

        # 7. Checkout (Place Order)
        checkout_url = reverse('checkout')
        response = self.client.post(checkout_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(float(response.data['total']), 99.95)
        self.assertEqual(len(response.data['items']), 1)
        self.assertEqual(response.data['items'][0]['product_name'], 'Test Product')
        self.assertEqual(response.data['items'][0]['quantity'], 5)

        # Verify cart is empty now
        response = self.client.get(cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)

        # 8. View Order History
        orders_url = reverse('order_list')
        response = self.client.get(orders_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['total']), 99.95)

        # 9. Test CartItem DELETE
        # Add another product to cart to test delete
        response = self.client.post(cart_url, {'product': self.product.id, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_cart_item_id = response.data['items'][0]['id']

        delete_url = reverse('cart_item_delete', kwargs={'pk': new_cart_item_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)
