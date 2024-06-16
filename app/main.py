import logging

from fastapi import FastAPI

from routes.memes import router as memes_router

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[
        # RotatingFileHandler("logs/bot.log", maxBytes=200000, backupCount=5),
        logging.StreamHandler(),
    ]
)
logging.getLogger("sqlalchemy").setLevel(level=logging.WARNING)
logging.getLogger("multipart.multipart").setLevel(level=logging.INFO)
logging.getLogger("httpcore").setLevel(level=logging.INFO)
logging.getLogger("httpx").setLevel(level=logging.INFO)

app = FastAPI(
    title="Memes API",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.1.0",
)

app.include_router(memes_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
