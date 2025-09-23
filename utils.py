
import pandas as pd
from twilio.rest import Client
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json



def get_date():

    input_date = datetime.now()
    input_date = input_date.strftime("%Y-%m-%d")

    return input_date

def request_weather_api(api_key,query):

    url_weather = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'

    try :
        response = requests.get(url_weather).json()
    except Exception as e:
        print(e)

    return response

def get_forecast(response,i):
    date = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]#Date
    hour = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condition = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']

    return date, hour, condition, tempe, rain, prob_rain

def create_df(data):

    columns=['Date','Hour','Condition','Temperature','Rain','Prob_rain']
    df = pd.DataFrame(data,columns=columns)
    df = df.sort_values(by = 'Hour',ascending = True)

    df_rain = df[(df['Rain']==1) & (df['Hour']>7) & (df['Hour']< 22)]
    df_rain = df_rain[['Hour','Condition']]
    df_rain.set_index('Hour', inplace = True)

    return df_rain

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df,query,PHONE_NUMBER,PHONE_RECEIVER):

    phoneNumb=PHONE_NUMBER
    receiver=PHONE_RECEIVER
    account_sid = TWILIO_ACCOUNT_SID 
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    if df.empty:
        body = f"Good morning, today's weather forecast ({input_date}) in {query} is:\n\n No rain today"
    else:
        body = f"Good morning, today's weather forecast ({input_date}) in {query} is:\n\n str({df})"


    message = client.messages.create(
                        body=body,
                        from_=phoneNumb,
                        to=receiver
                    )

    print(f'Message:\n {message.body}\n\nSent ({message.sid})')
