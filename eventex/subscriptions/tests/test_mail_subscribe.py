import uuid

from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Lucas', cpf='12345678901', email='contato@lucass.com.br',
                         phone='61-99210-0606', uuid=str(uuid.uuid3(uuid.NAMESPACE_DNS, '12345678901')))
        self.client.post('/inscricao/', self.data)
        self.mail = mail.outbox[0]

    def test_subscrition_email_subject(self):
        expect = "Confirmação de Inscrição"

        self.assertEquals(expect, self.mail.subject)

    def test_subscrition_email_from(self):
        expect = "contato@eventex.com.br"

        self.assertEquals(expect, self.mail.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'contato@lucass.com.br']

        self.assertEquals(expect, self.mail.to)

    def test_subscription_email_body(self):
        contents = [self.data['name'], self.data['cpf'],
                    self.data['email'], self.data['phone']]
        with self.subTest():
            for text in contents:
                self.assertIn(text, self.mail.body)
