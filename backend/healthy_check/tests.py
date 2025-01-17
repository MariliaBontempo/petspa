import pytest
from graphene_django.utils.testing import GraphQLTestCase

class TestHealthCheck(GraphQLTestCase):
    def test_graphql_healthcheck(self):
        query = '''
        query {
            healthCheck {
                status
            }
        }
        '''
        response=self.query(query)
        
        self.assertResponseNoErrors(response)
        content=response.json()
        self.assertEqual(content['data']['healthCheck']['status'], 'ok')
        