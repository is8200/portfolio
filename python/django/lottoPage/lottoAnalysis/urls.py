from django.urls import path

from . import views

app_name = 'lottoAnalysis'
urlpatterns = [
	#path('', views.index, name='index'),
	path('getStatistics/', views.getStatistics, name='getStatistics'),
	path('home/', views.home, name='home'),
]


