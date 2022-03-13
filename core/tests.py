# Import django test objects
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import make_aware

# Import required models 
from core.models import TodoList


# Create your tests here.
class LandingPageTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username':'user1',
            'password':'Ab@12345'
        }
        user = User.objects.create_user(**self.credentials)
        awared_datetime = make_aware(datetime.now())
        a = TodoList.objects.create(user=user, title='First Task', date_created=awared_datetime)
        b = TodoList.objects.create(user=user, title='Second Task', date_created=awared_datetime)
        
    def test_landing_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302) # Direct access redirects to Login page 


class AccountsAuthTest(LandingPageTest):
    def setUp(self):
        return super().setUp()

    def test_login(self):
        # Check if URL is working
        response = self.client.get('/accounts/login/') 
        # Try logging in with user created  
        login_res = self.client.post('/accounts/login/', **self.credentials, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(login_res.status_code, 200)
        # TODO: Try authenticate user after logging in  
        # self.assertTrue(login_res.context['user'].is_authenticated)


    def test_signUp(self):
        # Check if URL is working 
        response = self.client.get('/accounts/signup/')
        # Try creating a new account through POST request
        signUp_user_response = self.client.post('/accounts/signup/', {
            'username': 'testuser',
            'password1':'Ab@12345',
            'password2':'Ab@12345',
            'email':'testmail@mail.com'  # OPTIONAL
        }, follow=True)

        # Test if user created successfully and is logged in 

        self.assertTrue(signUp_user_response.context['user'].is_authenticated)
        self.assertEqual(TodoList.objects.filter(user__username='user1').count(), 2)
        self.assertEqual(TodoList.objects.filter(user__username='testuser').count(), 0)
    
    def test_signOut(self):
        response = self.client.get('/accounts/logout/')
        # Logging in before testing log out
        signUp_user_response = self.client.post('/accounts/signup/', {
            'username': 'testuser',
            'password1':'Ab@12345',
            'password2':'Ab@12345',
            'email':'testmail@mail.com'  # OPTIONAL
        }, follow=True)
        # Try logging out the user of current session
        
        logout_response = self.client.post('/accounts/logout/', follow=True)
        self.assertFalse(logout_response.context['user'].is_active)
        self.assertEqual(response.status_code, 302)
        
class DeleteTaskTest(LandingPageTest):

    def setUp(self):
        return super().setUp()
    
    def test_valid_delete_task(self):
        MAX_TASK_ID = TodoList.objects.latest('id').id
        response = self.client.get(f'mark/{MAX_TASK_ID}')
        self.assertEqual(response.status_code, 404)
"""
Model Fields for reference
"""
# user
# title
# date_created
# date_completed
# status

# from django.contrib.auth.models import User
# from django.test import TestCase

# class LogInTest(TestCase):
#     def setUp(self):
#         self.credentials = {
#             'username': 'testuser',
#             'password': 'secret'}
#         User.objects.create_user(**self.credentials)
#     def test_login(self):
#         # send login data
#         response = self.client.post('/accoutns/login/', self.credentials, follow=True)
#         # should be logged in now
#         self.assertTrue(response.context['user'].is_active)
