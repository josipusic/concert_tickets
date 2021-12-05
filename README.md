## Concert Tickets Web Shop


##### NOTES AND STEPS BEFORE STARTING LOCAL ENV
* clone the project and cd into its root
* provide your own stripe test credentials
* look for list of necessary env variables
  * listed in: concert_tickets/config/local/web/web.env
  * setup steps are described with using Docker and "make" Utility and without them

##### SETUP WITH DOCKER AND MAKE UTILITY
* ```make start``` - this command will:
  * generate local variables necessary for development on Linux
  * run docker-compose which will:
    * create and start postgres container
      * with initially created database (detail in concert_tickets/config/local/db/init.sql)
    * create and start backend container
      * migrate database changes
      * load data fixtures
      * serve api on 127.0.0.1:8000
* browse for 127.0.0.1:8000/api/docs/
    ###### Note: other useful make commands are inside Makefile

##### SETUP WITHOUT DOCKER AND MAKE UTILITY
* locally save env variables from concert_tickets/config/local/web/web.env
  * defaults (in settings.py) for all variables exist except for strip variables
  * if you follow next steps on setting up postgres, defaults should suffice
    and you don't need to save them locally except for stripe variables
* create postgres database
  * perform sql commands from concert_tickets/config/local/db/init.sql with psql or whatever
* cd into root of this project
  * ```python3 -m venv venv```
  * ```. venv/bin/activate```
  * ```pip install -r requirements.txt```
  * ```python manage.py migrate```
  * ```python manage.py loaddata */fixtures/*.json```
  * ```python manage.py runserver```

##### NOTES AND STEPS AFTER STARTING LOCAL ENV
* after local env is started you should have preloaded superuser
  * username: superuser
  * password: topsecret
* browse 127.0.0.1:8000/admin/
  * on /login/ enter superuser credentials
  * if you plan to test with this user create a token for him/her
  * create non staff and non superuser user(s) and token(s) for testing also
  * drf token authentication is used
    * "Token <token_str>" should be value of Authorization header key