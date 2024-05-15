import requests
import json
import asyncio
from telegram import Bot
import datetime

def send_request(url, method='GET', headers=None, params=None, data=None):
    try:
        response = requests.request(method, url, headers=headers, params=params, data=data)
        response.raise_for_status()
        return response.json()  # Parse response as JSON
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None  # Return None in case of error

async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

sent_items = set()
async def main():
    # Define the URL, method, headers, params, and data for your request
    url = 'https://csgoempire.com/api/v2/trading/items'
    method = 'GET'
    params = {'is_commodity': 'false', 'per_page': '100', 'page': '1', 'price_max_above': '-6', 'sort': 'asc', 'order': 'market_value', 'price_min': '1000'}
    headers = {'User-Agent': 'PostmanRuntime/7.39.0', 'Authorization': '72b508a8fe5de57cf78a361a5b0d9dd0'}
    counter = 1
    # Send the request
    response_json = send_request(url, method, headers, params)  # Now returns JSON directly
    print(response_json)
    if response_json is not None and 'data' in response_json:
        try:
            # Check if the item is not a commodity
            for item in response_json['data']:
                
                if isinstance(item, dict) and not item.get('is_commodity', False):
                    if item['id'] not in sent_items:
                    # Send a message via Telegram
                        bot_token = '7020838298:AAHOGeJxt6NwjaG9h4d8AMu_fcFhHuXwt4o'
                        chat_id = '6347554334'
                        now = datetime.datetime.now().replace(microsecond=0)
                        
                        message = f"COUNTER: {counter}\nItem: {item['market_name']}\nCurrent Price: {item['market_value']}\nSuggested price: {item['suggested_price']}\ndiscount: {item['above_recommended_price']}.\nDate and Time: {now.strftime('%d/%m/%Y %H:%M:%S')}\n------------------------------------------------------------------------------------"
                        counter += 1
                        await send_telegram_message(bot_token, chat_id, message)

        except json.JSONDecodeError as e:
            print(f"Failed to parse response as JSON: {e}")

if __name__ == '__main__':
    asyncio.run(main())
