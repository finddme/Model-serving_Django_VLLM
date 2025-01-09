from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

# 개발할때만 true
DEBUG = 'True'

# .env에 random SECRET_KEY 넣는 거
# .env 파일 경로 설정
env_path = Path(__file__).resolve().parent.parent / '.env'

if not env_path.exists():
    with open(env_path, 'w') as f:
        f.write('')

# .env 파일 로드
load_dotenv(env_path)

# SECRET_KEY 확인 및 생성
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            env_content = f.read()
    else:
        env_content = ''
    
    if 'SECRET_KEY' not in env_content:
        with open(env_path, 'a') as f:
            f.write(f'\nSECRET_KEY={SECRET_KEY}')


BASE_DIR = Path(__file__).resolve().parent.parent


# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = ['192.168.0.172', 'localhost', '127.0.0.1', '*']

# CORS settings
# CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  
    'app',  # api 실행 앱 이름
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'asgi.application'

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

