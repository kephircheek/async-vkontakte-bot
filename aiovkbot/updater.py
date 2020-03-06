from aiovkbot.dispatcher import Dispatcher
from aiovkbot.master import Master

import logging

from aiojobs.aiohttp import setup
from aiohttp import web

class Updater:
    """Upadates manager. Create http server app, Dispatcher and Master"""
    def __init__(self, token, confirmation_code, secret_key, version=None):

        self.__dispatcher = Dispatcher(
            master=Master(token, version),
            secret_key=secret_key,
            confirmation_code=confirmation_code
        )

    @property
    def dispatcher(self):
        return self.__dispatcher

    @property
    def app(self):
        """Asynchrone http server for workshop master

        Routes:
            index (post): vk group notification handler
        """

        async def notification_handler(request):
            update = await request.json()

            return await self.dispatcher.handle(request, update)

        async def shutdown(app):
            await self.dispatcher.close()

        app = web.Application()
        app.router.add_post('/', notification_handler) # route for recieve vk notification
        app.on_shutdown.append(shutdown)
        setup(app) # setup app for aiojobs background tasks

        return app

    def start_webhook(self, host='localhost', port=10001):
        web.run_app(self.app, host=host, port=port)

