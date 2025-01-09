from django.urls import path
from django.contrib import admin
from app import model_router 
from ninja import NinjaAPI

api = NinjaAPI(
    title="LLM API",
    description="Language Model API with vLLM",
    version="1.0.0",
    docs_url="/docs",
    # urls_namespace='api'  # namespace 추가
)

api.add_router("/model/", model_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]


