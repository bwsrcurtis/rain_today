import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.getenv('api_key')
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')

weather_params = {
    "lat": os.getenv('lat'),
    "lon": os.getenv('lon'),
    "appid": api_key,
    "exclude": "current,minutely,daily",
}


response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for x in weather_slice:
    condition_code = x["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔",
        from_=os.getenv('sending_num'),
        to=os.getenv('receiving_num'),
    )


print(message.status)
