# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Animal(models.Model):
    name = models.CharField(max_length=150)
    sound = models.CharField(max_length=100)

    def speak(self):
        return 'The {} says "{}"'.format(self.name, self.sound)
