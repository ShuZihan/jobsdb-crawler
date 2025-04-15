import asyncio
import functools
import time
import logging


def timing(func):
    if asyncio.iscoroutinefunction(func):

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()
            logging.info(
                f"[async] {func.__name__} executed in {end-start:.2f} seconds."
            )
            return result

        return async_wrapper

    else:

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            logging.info(
                f"[sync] {func.__name__} executed in {end - start:.2f} seconds."
            )
            return result

        return sync_wrapper
