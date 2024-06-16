import logging

from fastapi import FastAPI

from routes import media_router

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[
        # RotatingFileHandler("logs/bot.log", maxBytes=200000, backupCount=5),
        logging.StreamHandler(),
    ]
)
logging.getLogger("botocore").setLevel(logging.INFO)
logging.getLogger("multipart.multipart").setLevel(level=logging.INFO)
logging.getLogger("aiobotocore.regions").setLevel(level=logging.INFO)

app = FastAPI()

app.include_router(media_router)
