# Healcare blockchain platform

## Getting Started
This is a project support for viewing doctor and patient's information, The platform will provide the api for login, vote and feedback about doctor background.

### Prerequisites

Prestarting you should install:

```
Python3, virtualenv, pip, node, npm
```
[mySQL server](https://github.com/PyMySQL/mysqlclient-python/)

### Installing

## Backend

Virtualen environment 

```
virtualenv -p python3 <environment_name>
virtualenv -p python3 env
```

```
source env/bin/activate
```

Go to project directory
```
cd blockchainPlatform
```

Install reuqirements
```
pip installl -r reuqirements.txt
```

Goto webService/setting.py to setting your mySQL database:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'drinkBar',                      # Or path to database file if using sqlite3.
        'USER': 'root',
        'PASSWORD': '123456789@X',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
	}
}
```

Migrate
```
python manage.py migrate
```

Makemigration if need it or when something is changed
```
python manage.py makemigrations
```

To run project, after that check localhost:8000
```
python manage.py runserver
```
## FrontEnd
go to frontEnd directory
```
cd frontEnd
```

install node module
```
npm install
```
to run project on localhost:42000
```
npm start

or 

ng serve
```

## API documentations

```
http://localhost:8000/docs/
```

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

The code will follow PEP8 style

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used for webService
* [Angular](https://angular.io/) - The web framework used for frontEnd

## Authors

* **Hoang TN** - *Web developer* - [HoangTN](https://github.com/HoangJerry/)
