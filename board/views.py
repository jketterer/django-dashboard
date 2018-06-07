from django.shortcuts import render

import requests, collections, re


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/forecast?id=5211420&units=imperial&appid=d5179e0ba46f8a6782a5c7dd2b1b14dd'
    city = 'Sellersville'
    # request the API data and convert the JSON to Python data
    city_weather = requests.get(url.format(city)).json()

    # make arrays of min/max temps and descriptions
    highs = [[], [], [], [], [], []]
    lows = [[], [], [], [], [], []]
    descs = [[], [], [], [], [], []]
    codes = [[], [], [], [], [], []]

    # put all values in an array
    cnt = 0
    for i in range(0, 5):  # run once for each day

        # if there is no data left for current day, copy first section from next day
        if i == 0 & city_weather['list'][cnt]['dt_txt'].find("03:00:00") == 0:
            highs[i].append(city_weather['list'][cnt]['main']['temp_max'])
            continue

        # run through each 3hr section until new day
        while city_weather['list'][cnt]['dt_txt'].find("03:00:00") == -1:
            # adds info to day
            highs[i].append(city_weather['list'][cnt]['main']['temp_max'])
            cnt += 1

        # required to add the 03:00:00 data set
        highs[i].append(city_weather['list'][cnt]['main']['temp_max'])

        cnt += 1

    # same loop for lows
    cnt = 0
    for i in range(0, 5):

        if i == 0 & city_weather['list'][cnt]['dt_txt'].find("03:00:00") == 0:
            lows[i].append(city_weather['list'][cnt]['main']['temp_min'])
            continue

        while city_weather['list'][cnt]['dt_txt'].find("03:00:00") == -1: # 3AM for EST
            lows[i].append(city_weather['list'][cnt]['main']['temp_min'])
            cnt += 1

        lows[i].append(city_weather['list'][cnt]['main']['temp_min'])
        cnt += 1

    # same loop for descriptions
    cnt = 0
    for i in range(0, 5):

        if i == 0 & city_weather['list'][cnt]['dt_txt'].find("03:00:00") == 0:
            descs[i].append(city_weather['list'][cnt]['weather'][0]['main'])
            continue

        while city_weather['list'][cnt]['dt_txt'].find("03:00:00") == -1:
            descs[i].append(city_weather['list'][cnt]['weather'][0]['main'])
            cnt += 1

        descs[i].append(city_weather['list'][cnt]['weather'][0]['main'])
        cnt += 1

    # same loop for icon codes
    cnt = 0
    for i in range(0, 5):

        if i == 0 & city_weather['list'][cnt]['dt_txt'].find("03:00:00") == 0:
            codes[i].append(city_weather['list'][cnt]['weather'][0]['id'])
            continue

        while city_weather['list'][cnt]['dt_txt'].find("03:00:00") == -1:
            codes[i].append(city_weather['list'][cnt]['weather'][0]['id'])
            cnt += 1

        codes[i].append(city_weather['list'][cnt]['weather'][0]['id'])
        cnt += 1

    # functions to calculate max/min temp and most common description
    def calc_high_temp(arr):
        high = 0

        for i in arr:
            if i > high:
                high = i
        return high

    def calc_low_temp(arr):
        low = 200

        for i in arr:
            if i < low:
                low = i
        return low

    def get_description(arr):
        counter = collections.Counter(arr)  # put array into fancy counter
        counter = counter.most_common(1)  # get most common value
        clean = (re.sub('[^a-zA-Z]+', '', str(counter[0])))  # remove extras
        return clean

    def get_code(arr):
        counter = collections.Counter(arr)
        counter = counter.most_common(1)
        clean = str(counter)[2:5]  # extract 3 digit code from output
        return clean

    weather = {
        'city': city,
        'day1': {
            "high_temp": round(calc_high_temp(highs[0])),
            "low_temp": round(calc_low_temp(lows[0])),
            "description": get_description(descs[0]),
            "code": get_code(codes[0]),
        },
        "day2": {
            "high_temp": round(calc_high_temp(highs[1])),
            "low_temp": round(calc_low_temp(lows[1])),
            "description": get_description(descs[1]),
            "code": get_code(codes[1]),
        },
        "day3": {
            "high_temp": round(calc_high_temp(highs[2])),
            "low_temp": round(calc_low_temp(lows[2])),
            "description": get_description(descs[2]),
            "code": get_code(codes[2]),
        },
        "day4": {
            "high_temp": round(calc_high_temp(highs[3])),
            "low_temp": round(calc_low_temp(lows[3])),
            "description": get_description(descs[3]),
            "code": get_code(codes[3]),
        },
        "day5": {
            "high_temp": round(calc_high_temp(highs[4])),
            "low_temp": round(calc_low_temp(lows[4])),
            "description": get_description(descs[4]),
            "code": get_code(codes[4]),
        },
    }

    # news
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&category=technology&pageSize=5&'
       'apiKey=f16efa74a7af44858ce4327d27ec1a4d')

    # gets json data from url (news api)
    response = requests.get(url).json()

    headlines = {
        "one": response['articles'][0]['title'],
        "two": response['articles'][1]['title'],
        "three": response['articles'][2]['title'],
        "four": response['articles'][3]['title'],
        "five": response['articles'][4]['title'],
    }

    context = {'weather': weather, 'headlines': headlines}
    return render(request, 'board/index.html', context)
