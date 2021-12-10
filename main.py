import requests #to send HTTP requests to API
from twilio.rest import Client #to send SMS alert using TWILIO api

STOCK_NAME = 'TSLA' #Stock you what to get alert of
NEWS_KEY = '' #your NEWS API Authentication key (you can get it by create acc)
STOCK_KEY = '' #your STOCK API Authentication key (you can get it by create acc)

NEWS_ENDPOINT = 'https://newsapi.org/v2/everything' #your choice  of News API endpoint Here I have used newsapi
STOCK_ENDPOINT = 'https://www.alphavantage.co/query' #your choice of  Stocks API endpoint Here I have  used alphavantage

#after creating acc on twilio you get your own account id and token
account_sid = ''
auth_token = ''

NEWS_PARAMETER = {
    'q': STOCK_NAME,
    'apiKey': NEWS_KEY,

}

STOCK_PARAMETER = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_KEY,
}

news_response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETER)
news_response.raise_for_status()

news_data = news_response.json()
three_articles = news_data['articles'][:3] #you can change number of articles accounding to you preferences


stock_response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETER)
stock_response.raise_for_status()

stock_data = stock_response.json()["Time Series (Daily)"]
stock_data_list = [values for (key, values) in stock_data.items()]
yesterday_closing_data = (stock_data_list[0]['4. close'])

day_before_yesterday_closing_price = (stock_data_list[1]['4. close'])

difference = float(yesterday_closing_data) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percent = round((difference / float(yesterday_closing_data)) * 100)
formatted_article = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]




if abs(diff_percent) > 5:
    client = Client(account_sid, auth_token)

    for article in formatted_article:
        message = client.messages.create(
            body= f"{formatted_article}",
            from_='' #your own Twilio number you get after creating acc,
            to='' #phone number you want to get SMS alert on

# NOTE:
#           TO get SMS alert every morning 
#           1. you have to create acc on https://www.pythonanywhere.com.
#           2. Upload this file (main.py) in Files section.
#           3. After uploading double tab main.py and open bash console.
#           4. In bash console type 'Python3 main.py' to run your code.
#           5. Then move to the task section and set time according to your country timeline and in text box type 'Python3 main.py'
#           6. Press Create.
#           7. Now you will recieve SMS alert every day on your suggested time.


