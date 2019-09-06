from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionsForm


class SubscriptionFormTest(TestCase):
    def setUp(self):
        self.form = SubscriptionsForm()

    def test_form_has_field(self):
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(self.form.fields))