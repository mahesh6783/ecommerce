from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Product, Cart, Order, P_order
from datetime import date

class ShoppingAppTests(TestCase):

    def setUp(self): 
        self.user = User.objects.create(
            u_name="Test User",
            u_phone="1234567890",
            u_add="Test Address",
            u_gender="Other",
            u_email="test@example.com",
            u_pwd="testpass"
        )
 
        self.product = Product.objects.create(
            p_name="Test Product",
            p_price="100",
            p_rating=4,
            p_det="Test details",
            p_cat="Fashion",
            image="product_images/test.jpg"
        )

        self.client = Client()

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.u_email, "test@example.com")

    def test_product_creation(self):
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.p_name, "Test Product")

    def test_add_to_cart(self):
        cart = Cart.objects.create(
            u_id=self.user,
            p_id=self.product,
            c_date=date.today(),
            p_status="Available"
        )
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(cart.p_id.p_name, "Test Product")

    def test_create_order(self):
        order = Order.objects.create(
            u_id=self.user,
            o_date=date.today(),
            d_name=self.user.u_name,
            d_add=self.user.u_add,
            d_location="Test City",
            total_amout="100",
            p_status="dispatched"
        )
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.d_name, "Test User")

    def test_create_p_order(self):
        order = Order.objects.create(
            u_id=self.user,
            o_date=date.today(),
            d_name=self.user.u_name,
            d_add=self.user.u_add,
            d_location="Test City",
            total_amout="100",
            p_status="dispatched"
        )
        p_order = P_order.objects.create(
            o_id=order,
            p_id=self.product,
            p_name=self.product.p_name,
            p_image=self.product.image,
            p_quantity=1,
            p_price=self.product.p_price,
            p_subtital="100"
        )
        self.assertEqual(P_order.objects.count(), 1)
        self.assertEqual(p_order.p_name, "Test Product")

    def test_login_view(self):
        response = self.client.post('/login/', {'email': self.user.u_email, 'pass': self.user.u_pwd})
        self.assertEqual(response.status_code, 302) 


