import os

from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', default='1(4-0_#o1dd23#qnwk&_z67q()^dkdx730mrzi(z6s$ts3kc_q')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default='True').lower() == 'true'

ALLOWED_HOSTS = ['*']
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000',
# ]
# CORS_URLS_REGEX = r'^.*$'

# Application definition

INSTALLED_APPS = [
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_elasticsearch_dsl',
    'django_filters',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'pkt_fpk.middleware.MacObtain',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pkt_fpk.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'pkt_fpk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

PAO_URL = os.getenv('PAO_URL', default='http://test/')
PAO_USER = os.getenv('PAO_USER', default='test')
PAO_PASS = os.getenv('PAO_PASS', default='test')
PAO_FACE_URL = os.getenv('PAO_FACE_URL', default='http://test/')
PAO_VOICE_URL = os.getenv('PAO_VOICE_URL', default='http://test/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('ENGINE', default='django.db.backends.postgresql'),
#         'OPTIONS': {
#             'options': '-c search_path={}'.format(
#                 os.getenv('POSTGRES_DB', default='fpk,public')),
#         },
#         'NAME': os.getenv('DB_NAME', default='erd'),
#         'USER': PAO_USER,
#         'PASSWORD': PAO_PASS,
#         'HOST': os.getenv('DB_HOST', default='10.102.100.108'),
#         'PORT': os.getenv('DB_PORT', default='5432'),
#     },
# }

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.getenv('ELASTIC_HOSTS', default='10.102.100.111:9200')
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'pkt_fpk.permissions.IsAuthorized',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'static')

# MEDIA_URL = '/storage/fpk/' # value значение в базе
# MEDIA_ROOT = '/opt/vit_data/shd_nfs/lvm/fpk/' # Сюда сохранить

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520

INTERNAL_IPS = [
    '127.0.0.1',
]

ASM_ADDRESS = os.getenv('ASM_ADDRESS', default='srv-pv-1.ss:8072')

ASM_APIKEY = ""

MAC_LABEL = {
        '0': "test",
        '1': "test",
        '2': "test",
        '3': "test"
    }
