from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-^%&_xdy77h_o2bc!6c2=5hrsn)dkne=x=c*x=q8x(l%n=+b%53'
DEBUG = True

INSTALLED_APPS = [
    'django_fs_urls',
    'tests',
]

ROOT_URLCONF = 'django_fs_urls.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
