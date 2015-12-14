# README #

This is a prototype of a security Incident Information Sharing Tool.

### Get Started ###

* Install [Python](www.python.org) 3 (preferrably version 3.4 or higher)
* Install [pip](https://pypi.python.org/pypi/pip) (included by default in Python 3.4)
* Navigate to source folder
* Run "pip install -r requirements.txt"
* Start the server by running "python manage.py runserver"
* Access your instance at localhost:8000

If you want to access the admin panel, you need to run the following command, and provide the input asked for.
"python manage.py createsuperuser"

### How do I find my way arond? ###

* "/admin" gives you access to manipulating (almost) anything you (might) want
* "/manage/dashboard" gives you access to the dayly operations of an incident handler (that's the idea, anyway)
* "/api/1.0/..." gives you access to the API. Use the endpoints defined in the document

### Quality of Code ###

Due to this project primarily being a prototype, the code is hackable, but not neccessarily of top quality. The same goes for UI, which preferrably would be implemented using something like Angular and consuming the API directly, instead of deaply nested pages to handle simple operations.

### License ###
Apache License v2