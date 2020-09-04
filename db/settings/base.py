"""
Django settings for db project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'contacts_db.apps.ContactsDbConfig',
    'vehicles_db.apps.VehiclesDbConfig',
    'clientcars_db.apps.ClientcarsDbConfig',
    'sup_invoices.apps.SupInvoicesConfig',
    'stock.apps.StockConfig',
    'workorders.apps.WorkOrdersConfig',
    'landing_page.apps.LandingPageConfig',
    #'model_clone',
    'xhtml2pdf', #installed
    #'dal',
    #'dal_select2',
    #'django_addanother',
    #'django_select2',
    #'dal_admin_filters',
    'preferences',
    'admin_reorder',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    #'dynamic_preferences',
    #'dynamic_preferences.users.apps.UserPreferencesConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phone_field', #installed
    'django_extensions', #installed for management
]

USE_DJANGO_JQUERY = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'db.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'preferences.context_processors.preferences_cp',
            ],
        },
    },
]

WSGI_APPLICATION = 'db.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('zh-cn', u'简体中文'), # instead of 'zh-CN'
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

MEDIA_ROOT = 'uploads/'
MEDIA_URL = '/media/'

ADMIN_REORDER = (
    # Keep original label and models
    #'sites',

    # Reorder app models
    'auth',
    {'app': 'landing_page','label':'Settings', 'models': ('landing_page.GlobalPreference',)},

    # Exclude models
    {'app': 'contacts_db','label':'Contacts', 'models': ('contacts_db.Contact','contacts_db.Business',)},

    {'app': 'vehicles_db','label': 'Vehicle Models', 'models': ('vehicles_db.Vehicles',)},
    {'app': 'clientcars_db','label': 'Clients', 'models': ('clientcars_db.Client',)},
    {'app': 'stock','label': 'Inventory', 'models': ('stock.InventoryPart',)},
    {'app': 'sup_invoices','label':'Part Purchases', 'models': ('sup_invoices.SupplierInvoice','sup_invoices.SupplierInvoiceParts',)},
    {'app': 'workorders','label':'Work Orders', 'models': ({'model':'workorders.EstimationLine','label':'Estimations'},{'model':'workorders.WorkOrderLine','label':'Work Orders'},{'model':'workorders.InvoiceLine','label':'Invoices'},)},
    # Cross-linked models
    #{'app': 'auth', 'models': ('auth.User', 'sites.Site')},

    # models with custom name
    #{'app': 'auth', 'models': (
    #    'auth.Group',
    #    {'model': 'auth.User', 'label': 'Staff'},
    #)},
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

django_heroku.settings(locals())