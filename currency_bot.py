import requests
from datetime import date, timedelta
"""
script to get the current exchange rate for currencies
via API from FIXER.IO
and send it via TELEGRAM to the user
this scripts runs once a day on PYTHONANYWHERE.COM
"""

#to FIXER.io
_ACCESS_KEY = 'YOUR_FIXER_IO_KEY'

#Telegram keys
_BOT_TOKEN = 'YOUR_TELEGRAM_TOKEN'
_BOT_Chat_ID = 'CHAT_ID_ADRESSEE'


def telegram_bot_sendmessage(bot_token: str, bot_chatID: str, bot_message: str):
    """send message to telegram"""
    
    api_text = (
        f'https://api.telegram.org/bot{bot_token}'
        f'/sendMessage?chat_id={bot_chatID}'
        f'&parse_mode=Markdown&text={bot_message}'
        )

    r = requests.get(api_text)
    return r.json()


def get_current_exchange_rate():
    """latest information of exchange rate""" 
 
    web_api = (
        f'http://data.fixer.io/api/latest'
        f'? access_key={_ACCESS_KEY}'
        f'& format=1'
        f'& base=EUR'
        f'& symbols=GBP'
    )

    r = requests.get(web_api)
    return r.json()['rates']['GBP']


def get_weekly_high():
    """weekly high"""

    for i in range(1,8):
        hist_date = date.today() - timedelta(days=i)
        web_api = (
            f'http://data.fixer.io/api/{hist_date}'
            f'? access_key={ACCESS_KEY}'
            f'& base=EUR'
            f'& symbols=GBP'
        )

        r = requests.get(web_api)
        #weekly_high = r.json()['rates']['GBP'] if r.json()['rates']['GBP'] < weekly_high else weekly_high
        if i == 1 or r.json()['rates']['GBP'] < weekly_high:
            weekly_high = r.json()['rates']['GBP']
            
    return weekly_high


if __name__ == '__main__':
    #GBP in Euro
    message = (
        f'current exchange rate:\n 1 Pound = {1/get_current_exchange_rate():.3} Euro \n'
        f'best exchange rate last 7 days:\n 1 Pound = {1/get_weekly_high():.3} Euro'
    )
    #print(message)

    response = telegram_bot_sendmessage(_BOT_TOKEN, _BOT_Chat_ID, message)
    #print(response)