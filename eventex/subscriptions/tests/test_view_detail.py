from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscribeDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Lucas Gomes de Oliveira',
            cpf='72324414104',
            email='contato@lucass.com.br',
            phone='61-99210-0606'
        )
        self.resp = self.client.get('/inscricao/{}/'.format(self.obj.pk))

    def test_get(self):
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html_contents(self):
        contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class SubscribeNotFound(TestCase):
    def test_notfound(self):
        resp = self.client.get('/inscricao/0/')
        self.assertEquals(404, resp.status_code)