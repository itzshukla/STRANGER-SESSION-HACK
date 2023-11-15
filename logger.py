import logging

logging.basicConfig(format='[%(asctime)s - %(levelname)s] - %(name)s : %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


class AsyncioFilter(logging.Filter):
    def filter(self, record):
        if record.levelname == 'ERROR' and "Task was destroyed but it is pending!" in record.msg:
            return False
        return True


asyncio_logger = logging.getLogger('asyncio')
asyncio_logger.addFilter(AsyncioFilter())

logging.getLogger('telethon').setLevel(logging.WARNING)
logging.captureWarnings(True)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
