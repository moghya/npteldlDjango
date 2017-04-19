from django.conf.urls import url

from . import views
app_name = 'downloader'
urlpatterns = [
    url(r'^details/$',views.details, name='details'),
    url(r'^getLecture/$',views.getLecture,name='getLecture')
]