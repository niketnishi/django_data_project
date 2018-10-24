About the Project
----
* Implemented Highcharts for plotting data on bar and stacked bar chart.
* Implemented chaching using redis
* Used django custtom commands to load data from CSV file to sqlite database
----

Installation and configuration
----
Install ```requirements.txt``` in virtual environment.
```
$ pip install -r requirements.txt
```
##### Implement Highcharts
* Include the following CDN to include the Highcharts library.
```
<script src="https://code.highcharts.com/highcharts.src.js"></script>
```
* Important Links for Highcharts
```
https://docs.djangoproject.com/en/2.1/
https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
https://simpleisbetterthancomplex.com/tutorial/2018/04/03/how-to-integrate-highcharts-js-with-django.html
https://www.highcharts.com/demo/column-stacked
```
##### Redis installation & configuration
* Using Redis for cashing
```
$ sudo apt-get install redis-server   (Install redis-server)
$ sudo redis-server   (start redis server)
$ pip install redis   (Already installed in virtual environment)
```
* Check if redis-server is running or not
```
$ redis-cli ping
```
* Setting up settings.py for caching
```
CACHE_TTL = 60 * 15
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "dtp"
    }
}
```
* If Location is ```redis://127.0.0.1:6379/1``` then run following command to view the cached page.
```
$ redis-cli -n 1
$ keys *    (To view all the cached page)
$ flushall  (To clear all the cached pages)
```
* Important Links for Redis
```
https://realpython.com/caching-in-django-with-redis/
https://www.tutorialspoint.com/django/django_caching.htm
https://code.tutsplus.com/tutorials/how-to-cache-using-redis-in-django-applications--cms-30178
```
#### Setting up django on Ubuntu and some useful commands
```
$ pip install django
$ django-admin startproject django_data_project
$ python manage.py startapp data_project
$ python manage.py createsuperuser

$ python manage.py runserver
$ python manage.py runserver 8080
$ python manage.py runserver 0:8080      (0 is shortcut for 0.0.0.0)

$ python manage.py makemigrations
$ python manage.py makemigrations data_project    (For a particular app)
$ python manage.py sqlmigrate data_project 0001   (sql version of changes that is going to be applied on database)
$ python manage.py migrate    (Applies the staged changes to database)

$ python manage.py shell      (Perform database queries on CLI)
```
#### Django ORM methods
```
$ save()
$ update()
$ delete()
$ create()
$ count()
```
#### Running queries on django shell
For running queries
```
$ sudo apt-get install sqlite3
$ sqlite3
sqlite> from <app_name>.models import Choice, Question
```
```
sqlite> Question.objects.all()
sqlite> Question.objects.filter(id=1)
sqlite> Question.objects.filter(question_text__startswith='What')
sqlite> Entry.objects.get(headline__contains='Lennon')
```
##### Get the question that was published this year.
```
sqlite> from django.utils import timezone
sqlite> current_year = timezone.now().year
sqlite> Question.objects.get(pub_date__year=current_year)
```
##### An “exact” match  (exact)
```
sqlite> Entry.objects.get(headline__exact="Cat bites dog")
```
##### A case-insensitive match  (iexact)
```
sqlite> Blog.objects.get(name__iexact="beatles blog")
```
##### The following is identical to Question.objects.get(id=1).
Shortcut for primary-key exact lookups.
```
sqlite> Question.objects.get(pk=1)
```
##### Make sure our custom method worked.   (Calling a function on the fetched object)
```
sqlite> q = Question.objects.get(pk=1)
sqlite> q.was_published_recently()
```
##### Display any related object id
```
sqlite> q.choice_set.all()
sqlite> q.choice_set.create(choice_text='Not much', votes=0)

sqlite> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
sqlite> c.question
sqlite> q.choice_set.count()
```
