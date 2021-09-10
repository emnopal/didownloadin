from django.urls import path
from .views import (
    home,
    downloadable_parse_url
)

appname = "facebook_downloader"

urlpatterns = [
    path('', home, name='home'),
    path('<str:downloadable_url>', downloadable_parse_url, name='redirect'),
]
