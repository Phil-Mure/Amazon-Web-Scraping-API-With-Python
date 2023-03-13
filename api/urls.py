from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
	path('', views.react_django, name="api-overview"),
	path('scrap/<int:pk>', views.url_detail, name="api-overview"),
	path('home', views.home, name="home"),
]