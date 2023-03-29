from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests
import json


def get_photo(city, state):
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": PEXELS_API_KEY,
    }
    params = {
        "per_page": 1,
        "query": city + " " + state,
    }
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except (KeyError, IndexError):
        return {"picture_url": None}


def get_weather_data(city, state):
    #define an EARL
    url = "http://api.openweathermap.org/geo/1.0/direct"
    #Define some PRAMS q is the city state and Country (for this specific API), limit is defining how many we want, and the last thing is the api key
    params = {
        "q": f"{city}, {state}, US",
        "limit": 1,
        "appid": OPEN_WEATHER_API_KEY,
    }
    #getting the two things we defined above
    response = requests.get(url, params=params)
    #spit out likea RAAW webpage and converts it to JASON
    content = response.json()
    #try to get latitude and langitude if it exists
    try:
        latitude = content[0]["lat"]
        longitude = content[0]["lon"]
        #if it aint there, its square
    except (KeyError, IndexError):
        return None
    #new PRAMS for new EARL
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }
    #NEW EARL
    url = "https://api.openweathermap.org/data/2.5/weather"
    #NEW REPSONSE
    response = requests.get(url, params=params)
    #spit out likea RAAW webpage and converts it to JASON
    content = response.json()
    #return that shit
    return {
        "description": content["weather"][0]["description"],
        "temp": content["main"]["temp"]
    }
    #one fetches lat and lon, the other inputs those to get the weather
