from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from urllib import request as requestApi
from lottoAnalysis.LottoDataAnal import LottoDataAnal
import json

def home(request) :
	return render(request, 'lottoAnalysis/home.html')

def getStatistics(request) :
	try :
		sDate = request.GET['sDate']
		eDate = request.GET['eDate']
		xAxis = request.GET['xAxis']
		bonus = request.GET['containBonus']
	except (KeyError) :
		return render(request, 'lottoAnalysis/home.html')
	#template = loader.get_template('lottoAnalysis/getStatistics.html')

	lottoDataAnalysys = LottoDataAnal(startDate=sDate, endDate=eDate, isContainSecond=bonus)
	result = lottoDataAnalysys.getDatas(xAxis)
	
	context = {
		'result' : result,
	}

	return HttpResponse(json.dumps(context), content_type="application/json")
