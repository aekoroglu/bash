import json, requests, datetime

def gunler(gun):
    if gun == '0':
        return 'Pazar'
    elif gun == '1':
        return 'Pazartesi'
    elif gun == '2':
        return 'Salı'
    elif gun == '3':
        return 'Çarşamba'
    elif gun == '4':
        return 'Perşembe'
    elif gun == '5':
        return 'Cuma'
    elif gun == '6':
        return 'Cumartesi'
    else:
        return 'error: ' +str(gun)

def get_weather():
    req = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=40.997010&lon=29.036032&units=metric&exclude=currently,minutely,hourly&lang=tr&appid=xxxx', timeout=5)
    server = req.json()
    weather = ('Bugün hava %s° ve %s, ' % (server['current']['temp'],server['current']['weather'][0]['description']))

    i = 0
    while i < 5:
        i +=1
        dt = datetime.datetime.fromtimestamp(int(server['daily'][i]['dt'])).strftime('%w')
        if (i == 5):
            tmp_weather = ('%s günü de %s° ve %s olacak.' % (gunler(dt),server['daily'][i]['temp']['day'],server['daily'][i]['weather'][0]['description']))
        else:
            tmp_weather = ('%s %s° %s, ' % (gunler(dt),server['daily'][i]['temp']['day'],server['daily'][i]['weather'][0]['description']))
        weather += tmp_weather

    return weather
