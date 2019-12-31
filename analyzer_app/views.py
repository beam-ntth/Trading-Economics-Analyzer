from django.shortcuts import render
from django.http import HttpResponse
from gather_data import get_all_countries, get_all_gdp_indicators, get_data
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(os.path.join(BASE_DIR, 'static'), 'json')


# Create your views here.
def index(request):
    all_countries = get_all_countries()
    all_gdps = get_all_gdp_indicators()
    all_dict = {'countries' : all_countries, 'gdps' : all_gdps}
    return render(request, 'analyzer_app/index.html', context=all_dict)

def run(request):
    country = request.GET['country']
    country_2 = request.GET['country-2']
    indicator = request.GET['indicator']
    indicator_2 = request.GET['indicator-2']
    start_date = request.GET['start-date']
    end_date = request.GET['end-date']

    all_countries = get_all_countries()
    all_gdps = get_all_gdp_indicators()
    selected_countries = [country.lower(), country_2.lower()]
    all_dict = {'countries': all_countries, 'gdps': all_gdps, 'selected': selected_countries}

    get_data(country, country_2, indicator, indicator_2, start_date, end_date)

    return render(request, 'analyzer_app/index.html', context=all_dict)



