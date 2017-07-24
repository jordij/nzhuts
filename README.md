![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)

NZ Huts
=======

New Zealand huts, campsites and more.

```
                                   /\
                              /\  //\\
                       /\    //\\///\\\        /\
                      //\\  ///\////\\\\  /\  //\\
         /\          /  ^ \/^ ^/^  ^  ^ \/^ \/  ^ \
        / ^\    /\  / ^   /  ^/ ^ ^ ^   ^\ ^/  ^^  \
       /^   \  / ^\/ ^ ^   ^ / ^  ^    ^  \/ ^   ^  \       *
      /  ^ ^ \/^  ^\ ^ ^ ^   ^  ^   ^   ____  ^   ^  \     /|\
     / ^ ^  ^ \ ^  _\___________________|  |_____^ ^  \   /||o\
    / ^^  ^ ^ ^\  /______________________________\ ^ ^ \ /|o|||\
   /  ^  ^^ ^ ^  /________________________________\  ^  /|||||o|\
  /^ ^  ^ ^^  ^    ||___|___||||||||||||___|__|||      /||o||||||\       |
 / ^   ^   ^    ^  ||___|___||||||||||||___|__|||          | |           |
/ ^ ^ ^  ^  ^  ^   ||||||||||||||||||||||||||||||oooooooooo| |ooooooo  |
ooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

```

Getting up and running locally
------------------------------

Build the environment:

```
$ docker-compose -f local.yml build
```

Start:

```
$ docker-compose -f local.yml up
```

More tips at http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html

Settings
--------

http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

### Setting Up Your Users

* To create an **superuser account**, use this command:

  `$ docker-compose -f local.yml run django python manage.py createsuperuser`

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Remove all images and volumes
-----------------------------

```
$ docker-compose -f local.yml rm --all
```

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```
$ coverage run manage.py test
$ coverage html
$ open htmlcov/index.html
```

### Running tests with py.test:

```
$ py.test
```

### Live reloading and Sass CSS compilation

http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html


### Celery


This app comes with Celery.

To run a celery worker:

```
$ cd nzhuts
$ celery -A nzhuts.taskapp worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

Deployment
----------

The following details how to deploy this application.

### Docker

http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
