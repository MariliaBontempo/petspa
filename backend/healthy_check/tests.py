from django.test import TestCase
from graphene.test import Client
from config.schema import schema

class TestHealthCheck(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_graphql_healthcheck(self):
        query = '''
        query {
            healthCheck {
                status
            }
        }
        '''
        response = self.client.execute(query)
        
        self.assertNotIn('errors', response)
        self.assertEqual(response['data']['healthCheck']['status'], 'ok')