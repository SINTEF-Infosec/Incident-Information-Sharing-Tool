# README #

This is a prototype of a security Incident Information Sharing Tool (IIST).

## Installation
* Get the code: `git clone git@github.com:SINTEF-Infosec/Incident-Information-Sharing-Tool.git`
* Install Python 3
* [Install pip](https://pip.pypa.io/en/latest/installing.html) (if not included with you Python install)
* Navigate to source folder with your preferred command line
  client, the following items commands are highlighted in verbatim,
  prefixed with a short description of what that command achievies.
* Install dependencies: `pip install -r requirements.txt`
* Run initiall setup: `python manage.py setup`
* Configure instance: `python manage.py configure`
* Create user: `python manage.py createsuperuser` and follow the instructions
* Start server: `python manage.py runserver`
* Optional: Start another server: `python manage.py runserver 0.0.0.0:8800`

## Connect two instances of IIST -- A and B
* Add instance B as a provider of A by entering its API endpoint
* The two instances will now self configure to be able to exchange information

### How do I find my way arond? ###

* `/admin` gives you access to manipulating (almost) anything you (might) want
* `/manage/dashboard` gives you access to the dayly operations of an incident handler (that's the idea, anyway)
* `/api/1.0/...` gives you access to the API. Use the endpoints defined in the document

### Quality of Code ###

Due to this project primarily being a prototype, the code is hackable, but not neccessarily of top quality. The same goes for UI, which preferrably would be implemented using something like Angular and consuming the API directly, instead of deaply nested pages to handle simple operations.

### License ###
Apache License v2