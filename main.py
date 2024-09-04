from fastapi import FastAPI
from loguru import logger

from src.api.routes import router
from src.config import settings

app = FastAPI(debug=settings.debug)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Application has been stopped.")
