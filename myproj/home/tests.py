from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .forms import MyRegistrationForm

# Create your tests here.
class LoginTest(TestCase):
    username = 'temporary'
    password = 'temporary'
    passbad  = 'asdf'
    email = 'temporary@host.tld'
    def setUp(self):
        user = User.objects.create_user(self.username, email=self.email, password=self.password)
 
    def test_login_ok(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/', follow=True)
        user = User.objects.get(username=self.username)
        self.assertEqual(response.context['user'].username, self.username)

    def test_login_fail(self):  # fail for password not match
        self.client.login(username=self.username, password=self.passbad)
        response = self.client.get('/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        self.client.logout()
        response = self.client.get('/', follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

class MyRegistrationFormTest(TestCase):
    username = 'testregister'
    password = 'temporary'
    passbad  = 'asdf'
    email = username+'@host.tld'

    def test_register_ok(self):
        form_data = {'username': self.username, 'password1':self.password, 'password2':self.password, 'email':self.email}
        form = MyRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_fail(self):   # fail for password not match
        form_data = {'username': self.username, 'password1':self.password, 'password2':self.passbad, 'email':self.email}
        form = MyRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class RegisterTest(TestCase):
    username = 'testregister'
    password = 'temporary'
    passbad  = 'asdf'
    email = username+'@host.tld'

    def test_register_fail_wrongpass(self): # fail for password not match
        form_data = {'username': self.username, 'password1':self.password, 'password2':self.passbad, 'email':self.email, 'submit':'Register'}
        response = self.client.post(reverse("home:register"), form_data, follow=True)
        user = response.context['user']
        self.assertFalse(user.is_authenticated)

    def test_register_ok(self):
        form_data = {'username': self.username, 'password1':self.password, 'password2':self.password, 'email':self.email, 'submit':'Register'}
        response = self.client.post(reverse("home:register"), form_data, follow=True)
        user = response.context['user']
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, self.username)
        user = User.objects.get(username=self.username)
        self.assertEqual(user.username, self.username)

    def test_register_fail_dupname(self):   # fail for duplicate password
        self.test_register_ok()
        self.client.logout()
        form_data = {'username': self.username, 'password1':self.password, 'password2':self.password, 'email':self.email, 'submit':'Register'}
        response = self.client.post(reverse("home:register"), form_data, follow=True)
        user = response.context['user']
        self.assertFalse(user.is_authenticated)

