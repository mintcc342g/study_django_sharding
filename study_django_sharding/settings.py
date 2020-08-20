"""
Django settings for study_django_sharding project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ
from pathlib import Path
from django_sharding_library.settings_helpers import database_configs


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
ROOT_DIR = (
    environ.Path(__file__) - 2
)

env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)
if READ_DOT_ENV_FILE:
    env.read_env(str(ROOT_DIR.path(".env")))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r8+4y@9dxmwzz0&4x3csz)6e#z3zdxmykl9#^ll#04*lo)3v*0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'django_sharding',

    # local
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'study_django_sharding.urls'

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

WSGI_APPLICATION = 'study_django_sharding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = database_configs(databases_dict={
    'unsharded_databases': [
        {
            'name': 'default',
            'environment_variable': 'SUMMER_DATABASE_URL',
            'default_database_url': env('SUMMER_DATABASE_URL'), # sqlite:///./summer.sqlite3
        },
    ],
    'sharded_databases': [
        {
            'shard_group': 'user_group',                           # 샤드 그룹은 굳이 정해주지 않아도 됨.
            'name': 'user_g1',                                     # name은 실제 DB명을 안 써도 됨.
            'environment_variable': 'SUMMER_ONE_DATABASE_URL',     # env를 설정했다면, 이 db url을 가진 사용한 변수명 여기에 써주면 됨.
            'default_database_url': env('SUMMER_ONE_DATABASE_URL'),
        },
        {
            'shard_group': 'user_group',
            'name': 'user_g2',
            'environment_variable': 'SUMMER_TWO_DATABASE_URL',
            'default_database_url': env('SUMMER_TWO_DATABASE_URL'),
        },
    ],
})


from .sharding_functions import UserGroupBucketingStrategy         # 커스텀 전략
# from django_sharding_library.sharding_functions import 원하는 거  # 라이브러리에서 제공하는 전략을 사용하고 싶다면 여기서 import

# 버켓팅과 라우팅 전략을 설정할 수 있음.
# 설정하지 않을 경우 각각 디폴트 전략으로 적용됨.
# 버켓팅의 디폴트 전략은 RoundRobinBucketingStrategy
# 라우팅의 디폴트 전략은 PrimaryOnlyRoutingStrategy
DJANGO_SHARDING_SETTINGS = {
    ### 특정 샤드그룹에 버켓팅 전략을 적용할 때
    'user_group': {
        'SKIP_ADD_SHARDED_SIGNAL': True,                      # 이건 뭔지 모르겠음.
        'BUCKETING_STRATEGY': UserGroupBucketingStrategy(     # 각 그룹별로 다른 전략을 사용할 수 있음
            shard_group='user_group',
            databases=DATABASES,
            max_range=10,
        ),
        # 'ROUTING_STRATEGY': SomeRoutingStrategy(databases=DATABASES),  # 라우팅 전략도 여기에 선언해줌. 선언하지 않을 경우 디폴트 전략 사용됨.
    },

    ### 샤드그룹이 없는 쪽에도 버켓팅 전략을 주고 싶다면 default로 선언
    # 'default': {
    #     'SKIP_ADD_SHARDED_SIGNAL': True,
    #     'BUCKETING_STRATEGY': UserGroupBucketingStrategy(
    #         shard_group='user_group',
    #         databases=DATABASES,
    #         max_range=10,
    #     ),
    #     # 'ROUTING_STRATEGY': SomeRoutingStrategy(databases=DATABASES),        
    # }
}

DATABASE_ROUTERS = ['django_sharding_library.router.ShardedRouter']



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

DEBUG = True