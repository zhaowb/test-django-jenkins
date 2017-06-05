from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your tests here.
class UserProfileTest(TestCase):
    username = 'testprofile'
    password = username
    def test_update(self):
        # create a user
        user = User.objects.create_user(self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        form_data = {'attr1':True, 'attr2':'bbb'}
        response = self.client.post(reverse('userprofile:profile'), form_data, follow=True)
        profile = user.profile
        self.assertEqual(profile.attr1, form_data['attr1'])
        self.assertEqual(profile.attr2, form_data['attr2'])
