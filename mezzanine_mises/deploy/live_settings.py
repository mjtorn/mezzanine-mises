
DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "%(proj_name)s",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "127.0.0.1",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    },
    'django_mises': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/www/mises.fi/mises.db',
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

DEFAULT_FROM_ADDRESS = 'staff@mises.fi'

TIME_ZONE = 'Europe/Helsinki'

USE_L10N = True
LANGUAGE_CODE = 'fi'

DATE_FORMAT = 'l j.m.Y.'
TIME_FORMAT = 'h:i'
DATETIME_FORMAT = 'j.m.Y. h:i'

# EOF

