import asyncio
import aiohttp
import random
import logging

from aiovkbot.components import Keyboard

class Master:
    """Class matser to work with group api

    Example:
        >>> Master('...')
        VK bot with api version v5.80
    """

    DEFAULT_API_VERSION = '5.80'

    def __init__(self, token, version=None):
        self.__version = version or Master.DEFAULT_API_VERSION
        self.__token = token
        self.__api_url = "https://api.vk.com/method/"
        self.__static_keyboard = None
        self.__session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
        self.__context = dict()

    def __repr__(self):
        return f'VK bot with api version {self.__version}'

    def __getitem__(self, key):
        return self.__context[key]

    def __setitem__(self, key, val):
        self.__context[key] = val

    async def close(self):
        await self.__session.close()

    @property
    def _default_data(self):
        return {'v': self.__version, 'access_token': self.__token}

    def set_static_keyboard(self, keyboard):
        self.__static_keyboard = keyboard

    async def send_message(self, user_id, text=None, keyboard=None, drop_static_keyboard=False):
        """send message to `user` with `text`"""

        if not any([text, keyboard, self.__static_keyboard]):
            raise ValueError('Not enough input argurments. '
                             'Pass text or keyboard or set static keyboard')


        url = self.__api_url + 'messages.send/'

        data = self._default_data
        data['random_id'] = random.randint(0, 100_000_000)
        data['user_id'] = user_id
        data['message'] = text

        if (keyboard and not keyboard.inline) and not drop_static_keyboard:
            data['keyboard'] = str(keyboard + (self.__static_keyboard or Keyboard()))

        elif keyboard:
            data['keyboard'] = str(keyboard)

        print(data)
        resp = await self.__session.post(url, data=data)
        logging.debug(f"POST: {url.__repr__()}")
        logging.debug(f"Response [{resp.status}] {(await resp.text()).__repr__()}")

        logging.debug(f"Sent message to {data['user_id'].__repr__()} "
                      f"with text: {data['message'].__repr__()} "
                      f"and keyboard: {data.get('keyboard').__repr__()}")

        if keyboard and keyboard.inline and self.__static_keyboard and not drop_static_keyboard:
            await self.send_message(user_id, keyboard=self.__static_keyboard)

        return data['random_id']

