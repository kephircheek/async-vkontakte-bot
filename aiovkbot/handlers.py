import re
import json
import asyncio
import logging
from functools import wraps
from aiovkbot.errors import (PermissionDeniedError,
                     InvalidCommandError,
                     NotMatchPattern)

def rename(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__name__ = name
        return wrapper
    return decorator

def pattern(regexp):
    """
    """
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message, *args, **kwargs):
            if message.get('text') and re.search(regexp, message['text']):
                return await handler(message, *args, **kwargs)

            raise NotMatchPattern(f"Text are not satisfied the pattern `{pattern}`")
        return wrapper
    return decorator

def who(checker):
    """Parameterized decorator for permission restriction

    Args:
        checker (function): return True for permissible `user_id`
    """
    def decorator(handler):
        @wraps(handler)
        async def wrapper(message, *args, **kwargs):
            if checker(message['from_id']):
                return await handler(message, *args, **kwargs)

            raise PermissionDeniedError(f"Permission denied for user {message['from_id']}")
        return wrapper
    return decorator

def command(handler):
    """
    """
    @wraps(handler)
    async def wrapper(message, *args, **kwargs):
        if json.loads(message.get('payload', "{}")).get('command') == handler.__name__:
            logging.debug(f"Success: Handler '{handler.__name__}' match the command")
            return await handler(message, *args, **kwargs)

        raise InvalidCommandError(f"Handler '{handler.__name__}' does not match the command")
    return wrapper


if __name__ == "__main__":
    import doctest;

    loop = asyncio.get_event_loop()
    print(doctest.testmod(extraglobs={'loop': loop}))
    loop.close()



