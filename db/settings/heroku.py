"""
Production Settings for Heroku
"""

import environ
import dj_database_url
# If using in your own project, update the project namespace below
from db.settings.base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

POSTGRES_URL = env('HEROKU_POSTGRESQL_TEAL_URL')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}

DEFAULT_FILE_STORAGE = env('DEFAULT_FILE_STORAGE')
AWS_STORAGE_BUCKET_NAME = env('S3_BUCKET_NAME')
S3_BUCKET_NAME = env('S3_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = 'https://s3.amazonaws.com'

