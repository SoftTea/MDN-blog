# from django.test import TestCase

# # Create your tests here.

# class YourTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print("setUp: Run once for every test method to setup clean data.")
#         pass

#     def test_false_is_false(self):
#         print("Method: test_false_is_false.")
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print("Method: test_false_is_true.")
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print("Method: test_one_plus_one_equals_two.")
#         self.assertEqual(1 + 1, 2)

from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Blogger 

class BloggerModelTest (TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

        user.first_name = 'John'

        user.last_name = 'Citizen'

        Blogger.objects.create(user = user ,biography='This is a test!')

    def test_user_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('user').verbose_name
        self.assertEquals(field_label,'user')

    def test_biography_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('biography').verbose_name
        self.assertEquals(field_label,'biography')

    def test_biography_max_length(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('biography').max_length
        self.assertEquals(max_length, 1000)

    def test_object_name_is_user_object(self):
        blogger = Blogger.objects.get(id=1)
        expected_object_name = User.objects.get(id=1).username
        self.assertEquals(expected_object_name, str(blogger))

    def test_get_absolute_url(self):
        blogger = Blogger.objects.get(id=1)
        self.assertEquals(blogger.get_absolute_url(),'/posts/bloggers/1' )

    def test_help_text_biography (self):
        blogger = Blogger.objects.get(id=1)
        expected_text = blogger._meta.get_field('biography').help_text
        self.assertEquals('Biography for blogger info',expected_text)

    def test_ordering (self):
        blogger = Blogger.objects.get(id=1)
        expected_text = blogger._meta.ordering
        self.assertEquals(['user__username'],expected_text)
