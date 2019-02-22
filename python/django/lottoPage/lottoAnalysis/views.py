from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from urllib import request as requestApi
from lottoAnalysis.LottoDataAnal import LottoDataAnal
#from LottoDataAnal 

#from .models import Question

def index(request) :
	#last_question_list = Question.objects.order_by('-pub_date')[:5]
	latest_question_list = [{'id' : 1, 'question_text' : 'results'}, {'id' : 2, 'question_text' : 'results'}, {'id' : 3, 'question_text' : 'results'}, {'id' : 4, 'question_text' : 'results'}, {'id' : 5, 'question_text' : 'results'},]
	template = loader.get_template('lottoAnalysis/index.html')
	context = {
		'latest_question_list' : latest_question_list,
	}
	#return HttpResponse(template.render(context, request))
	#위와 아래는 같은거니까 알아서 사용해 
	return render(request, 'lottoAnalysis/index.html', context)

def results(request, question_id) :
	response = "Your are %s"
	return HttpResponse(response % question_id)

def home(request) :

	return render(request, 'lottoAnalysis/home.html')

def getStatistics(request) :
	pa_list = [{'id' : 1, 'question_text' : 'results'}, {'id' : 2, 'question_text' : 'results'}, {'id' : 3, 'question_text' : 'results'}, {'id' : 4, 'question_text' : 'results'}, {'id' : 5, 'question_text' : 'results'},]
	
	
	try :
		analType = request.POST['analType']
	except (KeyError) :
		analType = None
	#template = loader.get_template('lottoAnalysis/getStatistics.html')
	context = {
		'pa_list' : pa_list,
		'analType' : analType,
	}


	#lottoDataAnalysys = LottoDataAnal(startDate='2018-11-20')
	#lottoDataAnalysys.connection()

	return render(request, 'lottoAnalysis/getStatistics.html', context)
