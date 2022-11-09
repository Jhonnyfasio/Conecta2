import dj_database_url

from decouple import config


#DATABASES = {
#    'default': dj_database_url.config(
#        default=config('DATABASE_URL')
#    )
#}

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd68amv284hpn7n',
        'USER': 'ftlazppuqhna',
        'PASSWORD': '20c467abafb5c6d6f4294068e03fcfa9d4be28ed61419cb711392c34c69dc6f3',
        'HOST': 'ec2-34-233-157-189.compute-1.amazonaws.com',
        'DATABASE_PORT': '5432',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'gestionUsuarios',
    'api',
]