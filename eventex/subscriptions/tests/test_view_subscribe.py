from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionsForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

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
        data = dict(name='Lucas', cpf='72324414104',
                    email='contato@lucass.com.br', phone='61-99210-0606')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertEquals(302, self.resp.status_code)

    def test_send_email(self):
        self.assertEquals(1, len(mail.outbox))

    def test_save_subscribe(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

    def test_dont_save_subscribe(self):
        self.assertFalse(Subscription.objects.exists())


class SubscribeMessageSuccess(TestCase):
    def test_message(self):
        data = dict(name='Lucas', cpf='72324414104', email='contato@lucass.com.br', phone='61-99210-0606')
        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso')

