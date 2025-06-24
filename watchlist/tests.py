from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from watchlist.models import UserListItem, UserList
from django.db import IntegrityError

class UserListItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.userlist = UserList.objects.create(user=self.user)

    def test_userlistitem_requires_film(self):
        with self.assertRaises(IntegrityError):
            UserListItem.objects.create(userlist=self.userlist, film=None)

class SearchSessionTest(TestCase):
    def test_query_saved_to_session_on_search(self):
        response = self.client.get(reverse('watchlist:search_view'), {'q': 'Batman'})
        session = self.client.session
        self.assertIn('last_query', session)
        self.assertEqual(session['last_query'], 'Batman')

    def test_session_persists_query_across_pages(self):
        self.client.get(reverse('watchlist:search_view'), {'q': 'Batman'})

        response = self.client.get(reverse('watchlist:search_view') + '?page=2')
        session = self.client.session
        self.assertEqual(session.get('last_query'), 'Batman')