import asyncio
import logging.config

import settings

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


async def main():
    logger.info("start application")

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
