import json, requests
from datetime import date, timedelta

def get_corona_top10():
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.3'})
    req = session.get('http://api.coronatracker.com/v3/analytics/dailyNewStats?limit=10', timeout=10)
    server = req.json()

    corona_top10 = '```Country            Case       Death\n'
    count = 0
    for x in server:
        country = "{:<15}".format(x.get('country'))
        case = "{:<5}".format(x.get('daily_cases'))
        death = "{:<5}".format(x.get('daily_deaths'))
        count += 1
        if (count == len(server)):
            tmp_corona = "%s    %s      %s```" % (country,case,death)
        else:
            tmp_corona = "%s    %s      %s\n" % (country,case,death)
        corona_top10 += tmp_corona

    return corona_top10

def get_corona_today(country):
    sedate = date.today().strftime('%Y-%m-%d')
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.3'})
    req = session.get('http://api.coronatracker.com/v3/analytics/newcases/country?startDate=%s&endDate=%s&countryCode=%s' % (sedate,sedate,country), timeout=20)
    server = req.json()
    dict_check = not server
    if dict_check == False:
        status = "1"
        return status,server[0].get('country'),server[0].get('last_updated'),server[0].get('new_infections'),server[0].get('new_deaths'),server[0].get('new_recovered')
    else:
        status = "0"
        return status

def get_corona_yesterday(country):
    today = date.today().strftime('%Y-%m-%d')
    sedate = date.today() - timedelta(days=1)
    yesterday = sedate.strftime('%Y-%m-%d')
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.3'})
    req = session.get('http://api.coronatracker.com/v3/analytics/newcases/country?startDate=%s&endDate=%s&countryCode=%s' % (yesterday,today,country), timeout=20)
    server = req.json()
    dict_check = not server
    if dict_check == False:
        status = "1"
        return status,server[0].get('country'),server[0].get('last_updated'),server[0].get('new_infections'),server[0].get('new_deaths'),server[0].get('new_recovered')
    else:
        status = "0"
        return status
