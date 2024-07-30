import asyncio

from backend.warns import WarningsDB


'''loop = asyncio.get_event_loop()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)'''


def create_event_loop():
    try:
        loop = asyncio.get_event_loop()
        return loop
    except RuntimeError as _ex:
        if WarningsDB.NOT_CURRENT_EVENT_LOOP in str(_ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
