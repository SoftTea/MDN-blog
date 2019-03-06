
from django.test import TestCase
from django.urls import reverse 

from posts.models import Blogger
from django.contrib.auth.models import User

class BloggerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_bloggers = 13

        for blogger_id in range(number_of_bloggers):

            Blogger.objects.create(
                user= User.objects.create_user(f'user{blogger_id}', 'myemail@crazymail.com', 'mypassword'),
                biography=f'{blogger_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/posts/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/blogger_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogger_list']) == 10)

    