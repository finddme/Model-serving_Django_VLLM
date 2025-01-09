"""
uvicorn model_serving.asgi:application --host 0.0.0.0 --port 8000 --workers 4
workers: CPU 코어 수에 맞게 조정
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_asgi_application()

