from django.urls import path
from .views import (
    home,
    downloadable_parse_url,
    DiDownloadinAPI,
)

appname = "facebook_downloader"

urlpatterns = [
    path('', home, name='home'),
    path('<str:downloadable_url>', downloadable_parse_url, name='redirect'),
    path("api/didownloadin/", DiDownloadinAPI.as_view(), name="didownloadin API"),
]
