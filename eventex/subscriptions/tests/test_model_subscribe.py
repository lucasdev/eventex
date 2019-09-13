from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription


class Subscribe(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Lucas Oliveiraa',
            cpf='72324414104',
            email='lucass.web@gmail.com',
            phone='61-99210-0606'
        )
        self.obj.save()

    def test_save_subscribe(self):
        self.assertTrue(Subscription.objects.exists())

    def test_create_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)
