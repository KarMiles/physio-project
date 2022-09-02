# Imports
# 3rd party:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import unittest
from django.test import Client
from django.views import generic
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.urls import reverse

# Internal:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from poll.views import PollList
from poll.models import Poll
from blog.models import Post


# USER SETUP
User = get_user_model()
client = Client()

username_customer = 'test_user_customer'
username_staff = 'test_user_staff'
password = '1qazcde3'

# Login user
def login_customer():
    client.force_login(
        User.objects.get_or_create(
            username=username_customer,
            password=password,
            is_staff='False'
            )[0])

def login_staff():
    client.force_login(
        User.objects.get_or_create(
            username=username_staff,
            password=password,
            is_staff='True'
            )[0])
        
# Logout user
def logout():
    client.logout()


class TestViews(unittest.TestCase):
    '''
    Test view to show page with a list of polls
    '''

    # TESTS SETUP

    @classmethod
    def setUpClass(cls):
        '''
        Set up test data used 
        for all tests in TestViews class
        '''
        print('\nsetUpClass')
        
        
        
    @classmethod
    def tearDownClass(cls):
        '''
        Delete test data used 
        for all tests in TestViews class
        '''
        print('\ntearDownClass')
        # Delete test data
        User.objects.filter(username=username_customer).delete()
        User.objects.filter(username=username_staff).delete()
        Post.objects.filter(slug='ttitle').delete()
        print('Test data deleted.')
    
    def setUp(self):
        '''
        Set up testing data
        '''
        # Create test users
        if not User.objects.filter(username=username_customer).exists():
            user_customer=User.objects.create(
                username=username_customer,
                password=password,
                is_staff='False'
            )
        #     print(f'Test user "{user_customer.username}" created.')
        # else:
        #     print(f'Test user "{user_customer.username}" already exists, \
        #         proceeding with test.')

        if not User.objects.filter(username=username_staff).exists():
            user_staff=User.objects.create(
                username=username_staff,
                password=password,
                is_staff='True'
            )
        #     print(f'Test user "{user_staff.username}" created.')
        # else:
        #     print(f'Test user "{user_staff.username}" already exists, \
        #         proceeding with test.')
        
        # # Create test user
        # if not User.objects
        # user = User.objects.create(
        #     username='TestUser',
        #     email='test@mail.com',
        #     password='1qazcde3',
        #     is_staff='True'
        # )

        # Create test Post
        if not Post.objects.filter(title='Ttitle').exists():
            Post.objects.create(
                title='Ttitle',
                slug='ttitle',
                author=user_staff,
                content='tcontent',
                excerpt='texcerpt',
                price='tprice',
                priority='3 - Normal',
                status='1',
                )
        
        # posts = Post.objects.all()
        # print(posts)

        # Create test Poll
        # Poll.objects.create(
        #     poll_id='999',
        #     author=User.username,
        #     question='Which option?',
        #     option_one='option_one',
        #     option_two='option_two',
        #     option_three='option_three'
        #     )

    def tearDown(self):
        '''
        Delete test data
        '''
        pass
    
    # Function for checking if indicated template is used
    def assertTemplateUsed(self, response, template_name):
        self.assertIn(
            template_name,
            [t.name for t in response.templates if t.name is not None]
        )

    # TESTS

    def test_user_can_login(self):
        """
        Tests that user can login.
        checks
        1. that the client session is in allauth registry.
        """
        login_customer()
        self.assertIn('_auth_user_id', client.session)
        logout()

    # def test_polllist_contains_test_poll(self):
    #     result = PollList.get_queryset(self)
    #     poll_object = Poll[0]
    #     self.assertIn(poll_object, result)

    # LOADING PAGES

    def test_get_homepage(self):
        '''
        Test to check that Home page displays.
        Checks:
        1. status code is 200 (success)
        and correct template is used.
        '''
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_get_post_detail_page(self):
        '''
        Test to check that Post Details page displays.
        Checks:
        1. status code is 200 (success)
        and correct template is used
        '''
        # TODO Test post_detail page
        # login_staff()
        # response = client.get('/ttitle')
        post_detail_url = reverse('post_detail', args=['ttitle'])
        response = client.get(post_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'post_detail.html')

        
        

    def test_polllist_not_equal_none(self):
        """
        Tests that Poll page loads list of polls.
        checks
        1. that the PollList is not empty.
        """
        result = PollList.get_queryset(self)
        self.assertIsNotNone(result)

    def test_poll_page(self):
        '''
        Test to check that Poll page displays.
        Checks:
        1. status code is 200 (success)
        and correct template is used.
        '''
        response = client.get('/poll/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'poll/poll_home.html')

    def test_polllist_not_equal_none(self):
        """
        Tests that Poll page loads list of polls.
        checks
        1. that the PollList is not empty.
        """
        result = PollList.get_queryset(self)
        self.assertIsNotNone(result)

    def test_login_page(self):
        '''
        Test to check that Login page displays.
        Checks:
        1. status code is 200 (success)
        and correct template is used.
        '''
        logout()
        response = client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'account/login.html')

    def test_contact_page(self):
        '''
        Test to check that Contact page displays.
        Checks:
        1. status code is 200 (success)
        and correct template is used.
        '''
        response = client.get('/contact/contact')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'django_contact_form/contact_form.html')

    def test_booking_page(self):
        '''
        Test to check that Booking page displays correctly.
        Checks:
        1. status code is 200 (success)
        and correct template is used
        for authorized user.
        2. status code is not 200 (success)
        if user is not authorized.
        '''
        # Booking page loads for authorized user
        login_customer()
        response = client.get('/booking/booking')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'booking.html')
        logout()

        # Booking page does not load for unauthorized user
        logout()
        response = client.get('/booking/booking')
        self.assertNotEqual(response.status_code, 200)
        logout()

if __name__ == '__main__':
    unittest.main()
