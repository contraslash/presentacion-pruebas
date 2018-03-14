# Presentación sobre Pruebas Unitarias

[![CircleCI](https://circleci.com/gh/contraslash/presentacion-pruebas.svg?style=svg)](https://circleci.com/gh/contraslash/presentacion-pruebas)

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


## CI con CircleCI

Primero se autoriza a la aplicación a acceder a los repositorios desde el [marketplace de github](https://github.com/marketplace/circleci)

Luego se configura el repositorio para que CircleCI pueda configurar el ambiente.

CircleCI requiere que exista un archivo de configuración presente en [.circleci/config.yml](.circleci/config.yml) con el siguiente contenido

```yaml
# Python CircleCI 2.0 configuration file
#
# Check https://circleci.com/docs/2.0/language-python/ for more details
#
version: 2
jobs:
  build:
    docker:
      # specify the version you desire here
      # use `-browsers` prefix for selenium tests, e.g. `3.6.1-browsers`
      - image: circleci/python:3.6.1

      # Specify service dependencies here if necessary
      # CircleCI maintains a library of pre-built images
      # documented at https://circleci.com/docs/2.0/circleci-images/
      # - image: circleci/postgres:9.4

    working_directory: ~/repo

    steps:
      - checkout

      # Download and cache dependencies
      - restore_cache:
          keys:
          - v1-dependencies-{{ checksum "requirements.txt" }}
          # fallback to using the latest cache if no exact match is found
          - v1-dependencies-

      - run:
          name: install dependencies
          command: |
            python3 -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt

      - save_cache:
          paths:
            - ./venv
          key: v1-dependencies-{{ checksum "requirements.txt" }}

      # run tests!
      # this example uses Django's built-in test-runner
      # other common Python testing frameworks include pytest and nose
      # https://pytest.org
      # https://nose.readthedocs.io
      - run:
          name: run tests
          command: |
            . venv/bin/activate
            python manage.py test

      - store_artifacts:
          path: test-reports
          destination: test-reports

```

Como vemos, se requiere que exista un archivo con los requerimientos en [requirements.txt](requirements.txt)

Esto se logra usando el comando

```bash
pip freeze > requirements.txt
```

Finalmente para añadir el estado de la construcción, podemos añadir un badge a nuestro readme

```markdown
[![CircleCI](https://circleci.com/gh/contraslash/presentacion-pruebas.svg?style=svg)](https://circleci.com/gh/contraslash/presentacion-pruebas)
```