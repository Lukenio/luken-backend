import os
from os.path import join
from distutils.util import strtobool
import dj_database_url
from configurations import Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',


        # Third party apps
        'rest_framework',            # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_filters',            # for filtering rest endpoints
        'rest_registration',         # for registration and login endpoints
        'rest_framework_swagger',    # API documentation app
        'anymail',                   # sending mails api
        'corsheaders',               # disable cors during development stage
        "reversion",                 # app to track model changes

        # Your apps
        'luken.users',
        "luken.coins",
        "luken.loan",
        "luken.partners",
        "luken.xpub"
    )

    CORS_ORIGIN_ALLOW_ALL = True

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ALLOWED_HOSTS = ["*"]
    ROOT_URLCONF = 'luken.urls'
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    WSGI_APPLICATION = 'luken.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ADMINS = (
        ('Author', 'polinom100@gmail.com'),
    )

    # Postgres
    DATABASES = {
        'default': dj_database_url.config(
            default='postgres://postgres:@postgres:5432/postgres',
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        )
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = strtobool(os.getenv('DJANGO_DEBUG', 'no'))

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
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

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO'
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        )
    }

    REST_REGISTRATION = {
        'REGISTER_VERIFICATION_ENABLED': True,
        "REGISTER_VERIFICATION_URL": "/verify-account/",

        'RESET_PASSWORD_VERIFICATION_URL': '/reset-password/',

        'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
        'VERIFICATION_FROM_EMAIL': 'no-reply@example.com',
        "REGISTER_EMAIL_VERIFICATION_URL": "/verify-email/",
        "PROFILE_SERIALIZER_CLASS":
            "luken.users.serializers.UserProfileSerializer",

        'REGISTER_EMAIL_VERIFICATION_EMAIL_TEMPLATES': {
            'subject': 'rest_registration/register_email/subject.txt',
            'body': 'users/register_email.html',
        },

        'RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES': {
            'subject': 'rest_registration/reset_password/subject.txt',
            'body': 'users/reset_password.html',
        },

        'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
            'subject': 'rest_registration/register/subject.txt',
            'body': 'users/register.html',
        },

    }

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'basic': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        }
    }

    LOGIN_URL = 'rest_framework:login'
    LOGOUT_URL = 'rest_framework:logout'

    BLOCKCHAIN_XPUB = os.getenv("DJANGO_BLOCKCHAIN_XPUB")
    BLOCKCHAIN_API_KEY = os.getenv("DJANGO_BLOCKCHAIN_API_KEY")
    BLOCKCHAIN_CALLBACK_SECRET = os.getenv("DJANGO_BLOCKCHAIN_CALLBACK_SECRET")

    HOST_URL = os.getenv("DJANGO_HOSTNAME", "http://postb.in/RR1F5NB0")

    COIN_BACKENDS = {
        "Bitcoin": "luken.coins.services.BitcoinBackend",
        "Ethereum": "luken.coins.services.EthereumBackend",
    }

    TXHASH_API_KEY = os.getenv("DJANGO_TXHASH_API_KEY")
