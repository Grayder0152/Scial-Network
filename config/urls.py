from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/', include('posts.urls')),
]
