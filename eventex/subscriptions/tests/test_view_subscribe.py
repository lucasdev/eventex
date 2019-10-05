import uuid

from django.core import mail
from django.test import TestCase

from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionsForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get(r('subscriptions:new'))

    def test_get(self):
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_form.html')

    def test_html(self):
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        context = self.response.context['form']
        self.assertIsInstance(context, SubscriptionsForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Lucas Gomes de Oliveira', cpf='12345678901', email='contato@lucass.com.br',
                         phone='61-99210-0606', uuid=str(uuid.uuid3(uuid.NAMESPACE_DNS, '12345678901')))
        self.resp = self.client.post(r('subscriptions:new'), self.data)

    def test_post(self):
        self.assertRedirects(self.resp, r('subscriptions:detail', self.data['uuid']))

    def test_send_email(self):
        self.assertEquals(1, len(mail.outbox))

    def test_save_subscribe(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

    def test_dont_save_subscribe(self):
        self.assertFalse(Subscription.objects.exists())
