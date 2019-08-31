from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_home(self):
        self.assertEquals(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_inscricao_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')
