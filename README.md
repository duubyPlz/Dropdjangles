# Dropdjangles
This is a UNSW SENG2021 s2 Project

Supported browser: Google Chrome

Known not working: Firefox (Drag and Drop functionality not working)

### Dropjangles how-to-run

`sudo apt-get install postgresql postgresql-contrib postgresql-server-dev-9.3 python-dev python3-dev python-pip redis-server`  
`redis-server &`
> Write something like "asdf" to return back to shell while running redis in the background.

`sudo su postgres`  
`psql`  
`$ CREATE USER admin WITH PASSWORD 'admin';`  
`$ CREATE DATABASE timetable;`  
`$ GRANT ALL PRIVILEGES ON DATABASE timetable to admin;`  
`$ \q`  
`$ exit`  

* Navigate to Dropjangles/src 
* Recommended: Use `virtualenv` (will require sudo if not using `virtualenv` - not recommended)

`pip install -r requirements.txt`  
`pip install --upgrade django-crispy-forms`  

`python manage.py migrate auth`  
> Note: this will throw errors - that is expected due to the order in which things have to be migrated.

`python manage.py migrate`  
`python populate_timetable.py`  
`python populate_classes.py`  

> This takes a while depending on your laptop ~1 minute

`python manage.py runserver`  

* Connect using a browser to localhost:8000
