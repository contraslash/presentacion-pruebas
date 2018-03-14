# Presentación sobre Pruebas Unitarias

Repositorio para la demostración de el uso de pruebas unitarias en Django

Para crear este proyecto se usaron los siguientes comandos

```bash
mkvirtualenv presentacion_pruebas
pip install django
django-admin startproject proyecto
cd proyecto
django-admin startapp aplicacion
```

En el archivo [proyecto/settings.py](proyecto/settings.py) se añadió la línea `'aplicacion'` en el arreglo `INSTALLED_APPS`

Se copió el código fuente de las pruebas en el archivo [aplicacion/test.py](aplicacion/test.py) tomado de [la página oficial de pruebas en django](https://docs.djangoproject.com/en/2.0/topics/testing/overview/)

```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
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

```

Y se diseño el siguiente archivo en [aplicacion/models.py](aplicacion/models.py) para
cumplir con las pruebas

```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Animal(models.Model):
    name = models.CharField(max_length=150)
    sound = models.CharField(max_length=100)

    def speak(self):
        return 'The {} says "{}"'.format(self.name, self.sound)

```