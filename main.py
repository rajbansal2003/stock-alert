import requests
from twilio.rest import Client
# for twilio
account_sid = "ACb4edc941740b9dc03723f92ba6d8090b"
auth_token = "045900e71c1ca59015f4c55f467d7d10"
# for stock api
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "Q4TSFASI8AU1HO7R"
# for news api
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "5d2ff4700250489db3e2510600329143"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stocke_parameters = {
    "function": "TIME_SERIES_DAILY", # tell how data you want, daily, intraday, weekly etc.., uske according func name change ho jayega
    "symbol": STOCK, # this is for stock you want to find
    "apikey": STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=stocke_parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()] # here we get the list of all day values

yesterday_data = data_list[0] # we access the yesterday price dict
yesterday_closing_price = yesterday_data["4. close"] # get closing price
print("today: ",yesterday_closing_price)

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print("yesterday: ", day_before_yesterday_closing_price)

# finding the +ve difference
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
# print(difference)
up_down = None
if float(yesterday_closing_price) > float(day_before_yesterday_closing_price):
    up_down = "Up"
else:
    up_down = "Down"

diff_percent = round((difference/float(yesterday_closing_price)) * 100, 2)
print(diff_percent, "%")

    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if diff_percent > -1:
    news_parameters = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME, # on what you want your news
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"] # get all the articles
    three_articles = articles[:3] # just choose 3 of them
    # print(three_articles)

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    formatted_article = [f"{STOCK}: {diff_percent}%{up_down}\nHeadline: {article['title']}. \n\nBrief: {article['description']}" for article in three_articles]
    # twilio
    client = Client(account_sid, auth_token)  # making an object of the class client
    for article in formatted_article:
        message = client.messages.create(  # create a message to send
            body=article,
            from_='+12015524050',  # twilio number
            to='+919784142413'  # verified phone number
        )
        print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

