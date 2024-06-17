from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_current_weather(zipcode):

    weather_api_key = os.getenv("WEATHER_API_KEY")
    zipcode_api_key = os.getenv("ZIPCODE_API_KEY")


    zipcode_url = "https://app.zipcodebase.com/api/v1/search?apikey=" + zipcode_api_key + "&codes=" + zipcode + "&country=US"

    zipcode_results = requests.get(zipcode_url).json()
    
    
    state_code = (zipcode_results['results'][zipcode][0]['state_code'])
    
    lat = str(zipcode_results['results'][zipcode][0]['latitude'])
    lon = str(zipcode_results['results'][zipcode][0]['longitude'])
    weather_alerts = "https://api.weather.gov/alerts/active/area/"+ state_code
    weather_alert_response = requests.get(weather_alerts).json()
    if len(weather_alert_response['features']) == 0:
        alert_headline = "No current weather alerts in your state."
    else:
        alert_headline = str(weather_alert_response['features'][0]['properties']['headline'])   
    location = zipcode_results['results'][zipcode][0]['city']
    weather_api_url = "https://api.openweathermap.org/data/3.0/onecall?lat=" + lat + "&lon=" + lon + "&units=imperial&appid=" + weather_api_key
    
    air_pollutant_api_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={weather_api_key}"
    air_pollutant_response = requests.get(air_pollutant_api_url).json()
    
    weather_api_response = requests.get(weather_api_url).json()

    return weather_api_response, location, alert_headline, air_pollutant_response

def get_time(time):
    if time == 0:
        time = '12AM'
    elif time > 12:
        time -= 12
        time = str(time) + 'PM'
    elif time < 12:
        time = str(time) + 'AM'
    elif time ==12:
        time = str(time) + 'PM'
    return time

if __name__ == "__main__":
    print('\n*** Get current weather conditions ***\n')

    zipcode = input("Please enter your zip code: ")
    country_code = input("Please enter your country code: ")

    weather_data = get_current_weather(zipcode, country_code)

    print("\n")
    pprint('weather_data')


