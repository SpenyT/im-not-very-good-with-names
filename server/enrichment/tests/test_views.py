from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class EnrichmentViewTestCase(TestCase):
    """Test cases for enrichment API endpoints."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()

    def test_ping_endpoint(self):
        """Test ping endpoint returns success."""
        response = self.client.get('/api/enrichment/ping/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['app'], 'enrichment')

    # def next_test(self):
