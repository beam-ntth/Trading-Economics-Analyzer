# import tradingeconomics as te
import urllib.request
import matplotlib.pyplot as plt
import json, os, re
import numpy as np
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(os.path.join(BASE_DIR, 'static'), 'json')
IMAGES_DIR = os.path.join(os.path.join(BASE_DIR, 'static'), 'images')

def format_string(indicator):
    indicator = indicator.replace(' ', '%20')
    return indicator

def get_news(country, country_2):
    link_1 = 'https://tradingeconomics.com/' + country + '/news'
    link_2 = 'https://tradingeconomics.com/' + country_2 +'/news'

    url_link = urllib.request.urlopen(link_1)
    url_link_2 = urllib.request.urlopen(link_2)

    data_1 = url_link.read()
    data_2 = url_link_2.read()
    data_1 = str(data_1).replace('<', ' ')

    # print(data_1)
    print(re.findall('[\w]', str(data_1)))
    # print(data_2)


# 'https://api.tradingeconomics.com/historical/country/mexico/indicator/gdp%20annual%20growth%20rate/2015-01-01/2018-12-31?c=3inf9u3cugyyfzi:2g7ig0zs0akkywb&format=json'
def get_data(country, country_2, indicator, indicator_2, start_date, end_date):

    if os.path.exists(IMAGES_DIR + '/plot.png'):
        os.unlink(IMAGES_DIR + '/plot.png')
        plt.clf()

    plt.figure(figsize=(15,11), dpi=150, )
    plt.title(country + " vs " + country_2 + " - " + indicator)
    plt.ylabel("Indicator - " + indicator)
    plt.xlabel("Analysis from " + start_date + " to " + end_date)

    # formatting strings to be compatible with html query
    country_formatted = format_string(country.lower())
    country_2_formatted = format_string(country_2.lower())
    indicator = format_string(indicator.lower())
    indicator_2 = format_string(indicator_2.lower())
    link_1 = 'https://api.tradingeconomics.com/historical/country/' + country_formatted + '/indicator/' + indicator + '/' + start_date + '/' + end_date + '?c=3inf9u3cugyyfzi:2g7ig0zs0akkywb&format=json'
    link_2 = 'https://api.tradingeconomics.com/historical/country/' + country_2_formatted + '/indicator/' + indicator_2 + '/' + start_date + '/' + end_date + '?c=3inf9u3cugyyfzi:2g7ig0zs0akkywb&format=json'

    print(link_1)
    print(link_2)

    url_link = urllib.request.urlopen(link_1)
    url_link_2 = urllib.request.urlopen(link_2)

    my_data = json.load(url_link)
    my_data_2 = json.load(url_link_2)
    all_value = []
    all_values_2 = []
    all_dates = []
    all_dates_2 = []

    for values in my_data:
        if values['Value'] == 0:
            continue
        all_value.append(values['Value'])
        all_dates.append(values['DateTime'][:10])

    for values_2 in my_data_2:
        if values_2['Value'] == 0:
            continue
        all_values_2.append(values_2['Value'])
        all_dates_2.append(values_2['DateTime'][:10])

    print(all_value)
    print(all_values_2)

    plt.grid(True)
    plt.plot(all_value, label=country)
    plt.plot(all_values_2, label=country_2)
    plt.xticks(np.arange(len(all_value)), all_dates, rotation=45)
    plt.legend()
    plt.savefig(IMAGES_DIR + '/plot.png')

# Return a list of all countries
def get_all_countries():
    with open(JSON_DIR + "/countries.json", "r") as read_file:
        all_countries_data = json.load(read_file)


    all_countries = []
    for country in all_countries_data:
        all_countries.append(country['Country'])

    return all_countries

# Return a list of all indicators for gdp
def get_all_gdp_indicators():
    with open(JSON_DIR + "/gdp.json", "r") as read_file:
        all_gdp_data = json.load(read_file)

    all_gdps = []
    for gdp in all_gdp_data:
        all_gdps.append(gdp["Category"])

    return all_gdps

# Testing
if __name__ == '__main__':
    # get_all_countries()
    # get_data('mexico', 'sweden', 'gdp', 'gdp', '2010-01-01', '2018-12-31', '2010-01-01', '2018-12-31')
    # print(format_indicator('GDP Annual Growth Rate'))
    # get_news('thailand', 'mexico')
    print(os.path.join(BASE_DIR, 'static'))