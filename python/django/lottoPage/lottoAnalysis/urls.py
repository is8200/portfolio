from django.urls import path

from . import views

app_name = 'lottoAnalysis'
urlpatterns = [
	path('', views.index, name='index'),
	path('<int:question_id>/results', views.results, name='results'),
]


