import logging
import asyncio
from aiohttp import web
from aiojobs.aiohttp import spawn

from aiovkbot.errors import (PermissionDeniedError,
                     InvalidCommandError,
                     NotMatchPattern)

class Dispatcher:
    """Handlers dispatcher. Store update handlers"""

    NEW_MESSAGE_NOTIFICATION = 'message_new'
    REPLY_MESSAGE_NOTIFICATION = 'message_reply'
    CONFIRMATION_REQUEST = 'confirmation'

    def __init__(self, master, confirmation_code, secret_key):
        self.__master = master
        self.__confirmation_code = confirmation_code
        self.__secret_key = secret_key
        self.__message_handlers = list()
        self.__default_message_handler = None

    async def close(self):
        await self.__master.close()

    def master(self):
        return self.__master

    def add_static_keyboard(self, keyboard):
        self.__master.set_static_keyboard(keyboard)

    def add_default_message_handler(self, handler):
        self.__default_message_handler = handler

    def add_message_handler(self, handler):
        self.__message_handlers.append(handler)

    async def handle(self, request, update):
        logging.debug(f'Update: {update}')
        if update['type'] == Dispatcher.CONFIRMATION_REQUEST:
            logging.debug(f'Responce confirmation code: {self.__confirmation_code}')
            return web.Response(text=self.__confirmation_code)

        elif update['type'] == Dispatcher.NEW_MESSAGE_NOTIFICATION:
            logging.debug(f"Handle as new message with id={update['object']['id']}")
            await spawn(request, self.__message_handle(update['object']))
            return web.Response(text='ok')

        elif update['type'] == Dispatcher.REPLY_MESSAGE_NOTIFICATION:
            logging.debug(f"Handle as 'reply message' {update['object']}")
            logging.debug("Nothing done!")
            return web.Response(text='ok')

        else:
            logging.warning(f"Unknown update type: {update['type']} in update: {update}")
            return web.Response(text='ok')

    async def __message_handle(self, message):
        for handler in self.__message_handlers:
            try:
                logging.debug(f"Try with handler '{handler.__name__}'")
                return await handler(message, self.__master)

            except InvalidCommandError as e:
                logging.debug(e)
                continue

            except NotMatchPattern as e:
                logging.debug(e)
                continue

            except PermissionDeniedError as e:
                logging.debug(e)
                if self.__permission_denied_error_handler:
                    return await self.__permission_denied_error_handler(message, self.__master)

                else:
                    continue

        if self.__default_message_handler:
            logging.warning(f"All hanlers are missing. Default handler triggered.")
            return await self.__default_message_handler(message, self.__master)

