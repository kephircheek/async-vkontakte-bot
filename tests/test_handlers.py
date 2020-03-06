import unittest
import asyncio
from aiovkbot.handlers import who, command, pattern, rename
from aiovkbot.errors import InvalidCommandError, PermissionDeniedError, NotMatchPattern

class TestHandlers(unittest.IsolatedAsyncioTestCase):

    async def test_command(self):

        @command
        async def test(message, *args):
            await asyncio.sleep(1)
            return True

        self.assertTrue(await test({'payload': '{\"command\":\"test\"}'}))
        with self.assertRaises(InvalidCommandError):
            await test({'payload': '{\"command\":\"other\"}'})


    async def test_who(self):

        def iseven(user_id):
            return True if user_id % 2 else False

        @who(iseven)
        async def test(message, *args):
            await asyncio.sleep(1)
            return True

        self.assertTrue(await test({'from_id': 1}))
        with self.assertRaises(PermissionDeniedError):
            await test({'from_id': 0})

    async def test_textfilter(self):

        @pattern(r'I am a \w+')
        async def test(message, *args):
            await asyncio.sleep(1)
            return True

        self.assertTrue(await test({'text': 'I am a Human'}))
        with self.assertRaises(NotMatchPattern):
            await test({'text': 'You are a Bot'})


    async def test_rename(self):

        @rename('foo')
        async def test():
           return

        self.assertEqual(test.__name__, 'foo')
