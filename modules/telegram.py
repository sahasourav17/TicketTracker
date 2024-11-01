import requests
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def send_notification(msg: str, TELEGRAM_BOT_API_KEY: str, TELEGRAM_CHAT_ID: str):
    '''
    How to get the TELEGRAM_BOT_API_KEY and TELEGRAM_CHAT_ID?
    1. search for BotFather in Telegram
    2. write command /start
    3. write command /newbot
    4. give it a name
    5. give it an unique username (ends with _bot)
    6. copy the API token: For example 5401329997:AAF2ZHcsn93lj_qkqKGYyZRNNYC_isV_Vh8

    7. Now create a channel/group in Telegram
    8. Make the bot an admin of the channel
    9. Send a hello message in the channel
    10. Go to the url https://api.telegram.org/bot{API_KEY}/getUpdates to get the chat_id, for example -1002119021579
    '''

    url = f'https://api.telegram.org/bot{
        TELEGRAM_BOT_API_KEY}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={msg}'

    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        logger.error('Failed to send message to Telegram')
        logger.error(response.json())
    return False
