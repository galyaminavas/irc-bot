from weather import Weather, Unit
import random


places_WOEID = [
    2459115,  # NYC
    2122265,  # Moscow
    560743,  # Dublin
    1118370,  # Tokyo
    638242,  # Berlin
    721943,  # Rome
    2347570,  # Hawaii
    2122851,  # Petergof
    2514815,  # Washington
    924938,  # Kyiv
    834463,  # Minsk
    615702,  # Paris
    7224124,  # Kaliningrad
    2122641,  # Omsk
    2442047,  # Los Angeles
    1105779,  # Sydney
    12597598,  # Izhevsk
    2345711  # Bali
]


def get_random_weather():
    rand_WOEID = places_WOEID[random.randrange(len(places_WOEID))]
    message = get_weather_msg(rand_WOEID)
    return message
    # for w in places_WOEID:
    #     print_weather(w)


def get_weather_msg(w):
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup(w)
    condition = location.condition
    msg = []
    msg.append(condition.date)
    msg.append('Weather in ' + location.location.city + ', ' + location.location.country)
    msg.append(condition.temp + '; ' + condition.text)
    return msg
    # print(condition.date)
    # print('Weather in ' + location.location.city + ', ' + location.location.country)
    # print(condition.temp + '; ' + condition.text)
