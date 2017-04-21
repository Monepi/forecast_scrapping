import requests


def get_weather():
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?id=3369157&units=metric&cnt=7&appid=466a2d0c5a6d7a56d27c16bfc95ae658"
    response = requests.get(url)
    return response
