from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Lucas', cpf='72324414104',
                    email='contato@lucass.com.br', phone='61-99210-0606')
        self.client.post('/inscricao/', data)
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
        contents = [
            'Lucas', '72324414104', 'contato@lucass.com.br', '61-99210-0606'
        ]
        for text in contents:
            with self.subTest():
                self.assertIn(text, self.mail.body)