import os
from twilio.rest import Client
import twilio_config

from tqdm import tqdm
import time
from utils import *
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import requests
from datetime import datetime


query = 'Zapopan'
api_key = twilio_config.API_KEY_WAPI

input_date= get_date()
response = request_weather_api(api_key,query)

data = []

for i in tqdm(range(24),colour = 'green'):

    data.append(get_forecast(response,i))


df_rain = create_df(data)

send_message(twilio_config.TWILIO_ACCOUNT_SID,twilio_config.TWILIO_AUTH_TOKEN,input_date,df_rain,query, twilio_config.PHONE_NUMBER, twilio_config.PHONE_RECEIVER)

