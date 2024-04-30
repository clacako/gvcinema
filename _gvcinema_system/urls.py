from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("gvcinema/movie/", include(("gvcinema.movies.urls", "movie"), namespace="movie"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

