from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import University


class UniversityAPITests(APITestCase):

    def setUp(self):
        # Create some universities with different ratings, locations and contract prices
        self.uni1 = University.objects.create(
            name="Alpha University",
            rating=10,
            min_contract=5000000,
            max_contract=15000000,
            location="tashkent_city",
            university_type="private"
        )
        self.uni2 = University.objects.create(
            name="Beta University",
            rating=50,
            min_contract=7000000,
            max_contract=20000000,
            location="samarkand",
            university_type="state"
        )
        self.uni3 = University.objects.create(
            name="Gamma University",
            rating=30,
            min_contract=6000000,
            max_contract=18000000,
            location="tashkent_city",
            university_type="state"
        )

    def test_university_fields_added(self):
        """Test if the new fields are successfully added to the database."""
        uni = University.objects.get(id=self.uni1.id)
        self.assertEqual(uni.min_contract, 5000000)
        self.assertEqual(uni.max_contract, 15000000)

    def test_paginated_api_response_structure(self):
        """Test that the paginated endpoint returns standard DRF paginated structure."""
        url = reverse('universities:university_list_paginated')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)
        
        # Check that we have 3 universities
        self.assertEqual(response.data['count'], 3)
        
        # Check first item contains new fields
        first_item = response.data['results'][0]
        self.assertIn('min_contract', first_item)
        self.assertIn('max_contract', first_item)
        self.assertEqual(first_item['min_contract'], 5000000)
        self.assertEqual(first_item['max_contract'], 15000000)

    def test_not_sorted_by_rating(self):
        """
        Verify that the list is NOT sorted by rating (default meta ordering),
        but by ID or other ordering specified in queryset.
        """
        # The regular non-paginated view: UniversityListView has default Meta ordering which is rating descending: [uni2 (50), uni3 (30), uni1 (10)]
        url_non_paginated = reverse('universities:university_list')
        res_non_paginated = self.client.get(url_non_paginated)
        ratings_non_paginated = [item['rating'] for item in res_non_paginated.data]
        self.assertEqual(ratings_non_paginated, [50, 30, 10])

        # The new paginated view is ordered by ID, so it should be [uni1, uni2, uni3] which has ratings [10, 50, 30]
        url_paginated = reverse('universities:university_list_paginated')
        res_paginated = self.client.get(url_paginated)
        ratings_paginated = [item['rating'] for item in res_paginated.data['results']]
        self.assertEqual(ratings_paginated, [10, 50, 30])

    def test_location_filtering(self):
        """Verify that exact-match location filtering works correctly."""
        url = reverse('universities:university_list_paginated')
        response = self.client.get(url, {'location': 'tashkent_city'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        names = [item['name'] for item in response.data['results']]
        self.assertIn("Alpha University", names)
        self.assertIn("Gamma University", names)
        self.assertNotIn("Beta University", names)
