from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionsForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_form.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        context = self.response.context['form']
        self.assertIsInstance(context, SubscriptionsForm)

    def test_form_has_field(self):
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Lucas', cpf='72324414104',
                    email='contato@lucass.com.br', phone='61-99210-0606')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        self.assertEquals(302, self.response.status_code)

    def test_send_email(self):
        self.assertEquals(1, len(mail.outbox))

    def test_subscrition_email_subject(self):
        expect = "Confirmação de Inscrição"

        self.assertEquals(expect, mail.outbox[0].subject)

    def test_subscrition_email_from(self):
        expect = "contato@eventex.com.br"

        self.assertEquals(expect, mail.outbox[0].from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'contato@lucass.com.br']

        self.assertEquals(expect, mail.outbox[0].to)

    def test_subscription_email_body(self):
        self.assertIn('Lucas', mail.outbox[0].body)
        self.assertIn('72324414104', mail.outbox[0].body)
        self.assertIn('contato@lucass.com.br', mail.outbox[0].body)
        self.assertIn('61-99210-0606', mail.outbox[0].body)


class SubscribeInvalidePost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionsForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubscribeMessageSuccess(TestCase):
    def test_message(self):
        data = dict(name='Lucas', cpf='72324414104', email='contato@lucass.com.br', phone='61-99210-0606')
        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso')

