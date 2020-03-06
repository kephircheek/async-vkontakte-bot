import os

import logging
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.DEBUG
)

import sys; sys.path.append('../')
print(*sys.path, sep='\n')

from aiovkbot import Updater

from dotenv import load_dotenv
load_dotenv() # before create `.env`

async def echo(message, bot):
    text = message['text']
    await bot.send_message(
        user_id=message['from_id'],
        text=f"{text}-{text[-3:]}-{text[-3:]}..."
    )

updater = Updater(
    token=os.getenv('TOKEN') or input('TOKEN='),
    confirmation_code=os.getenv('CONFIRMATION_CODE') or input('CONROMATION_CODE='),
    secret_key=os.getenv('SECRET_KEY') or input('SCRET_KEY='),
)

dp = updater.dispatcher
dp.add_default_message_handler(echo)

if __name__ == '__main__':
    import logging
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
    updater.start_webhook()
