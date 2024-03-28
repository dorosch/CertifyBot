import os
import pathlib


BASE_PATH = pathlib.Path(__file__).parent.resolve()
PROJECT_PATH = BASE_PATH.parent.resolve()

POSTGRES_DB = os.environ.get("POSTGRES_DB", "database")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "__main__": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        },
        "aiogram": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False
        }
    }
}

SUPPORTED_COURCES = {
    "DVA-C02": {
        "NAME": "AWS Certified Developer - Associate (DVA-C02)",
        "BADGE": PROJECT_PATH / "images" / "cource/AWS-Certified-Developer-Associate.png",
        "QUESTIONS": BASE_PATH / "migrations" / "fixtures" / "AWS-Developer-Associate-DVA-C02.json"
    },
    "SAA-C03": {
        "NAME": "AWS Certified Solutions Architect - Associate (SAA-C03)",
        "BADGE": PROJECT_PATH / "images" / "cource/AWS-Certified-Solutions-Architect-Associate.png",
        "QUESTIONS": BASE_PATH / "migrations" / "fixtures" / "AWS-Solutions-Architect-Associate-SAA-C03.json"
    }
}
