
from django.test import TestCase
from django.urls import reverse 

from posts.models import Blogger , Blog 
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

    def test_lists_all_bloggers(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('bloggers')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['blogger_list']) == 3)




class BlogsByLoggedInUserListViewTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        blogger1 = Blogger.objects.create(user=test_user1,biography='test1')
        blogger2 = Blogger.objects.create(user=test_user2, biography='test2')

        blogger1.save()
        blogger2.save()

        number_of_blogs = 30

        for blogs in range(number_of_blogs):
            Blog.objects.create(
                title = blogs,
                user = blogger2,
                content = 'This is content'
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my-blog'))
        self.assertRedirects(response, '/accounts/login/?next=/posts/myblog')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-blog'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'posts/blogs_by_user_loggedIn.html')

    def test_only_user_blogs_in_list(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my-blog'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        self.assertTrue('blog_list' in response.context)
        self.assertEqual(len(response.context['blog_list']), 0)

        self.assertEqual(str(response.context['user']), 'testuser1')

        self.assertEqual(response.status_code, 200)

        login2 = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')

        response = self.client.get(reverse('my-blog'))

        self.assertTrue('blog_list' in response.context)
        self.assertEqual(len(response.context['blog_list']), 10)
