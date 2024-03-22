import os


POSTGRES_DB = os.environ.get("POSTGRES_DB", "database")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "0.0.0.0")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        '__main__': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
