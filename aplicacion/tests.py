# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

from django.contrib.auth.models import User
from aplicacion.models import Animal


class AnimalTestCase(TestCase):
    """
    Tomado de https://docs.djangoproject.com/en/2.0/topics/testing/overview/
    """
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')


class LogInTestCase(TestCase):
    """
    Tomado de https://docs.djangoproject.com/en/2.0/topics/testing/tools/
    """
    def setUp(self):
        User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_log_in(self):
        c = Client()
        response = c.get('/')

        self.assertEqual(response.status_code, 302)

        c.post('/login/', {'username': 'test', 'password': 'test'})

        response = c.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "You're logged in")
