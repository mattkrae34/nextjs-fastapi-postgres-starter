import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from utils.db_utils import seed_user_if_needed
from utils.custom_logging import setup_logging
from routes.users import router as users_router
from routes.conversations import router as conversations_router

setup_logging()
logger = logging.getLogger(__name__)


# fast api app lifecycle hook see: https://fastapi.tiangolo.com/advanced/events/
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI server starting...")
    seed_user_if_needed()
    yield
    logger.info("FastAPI server shutting down...")


app = FastAPI(lifespan=lifespan, root_path="/api")

app.include_router(users_router)
app.include_router(conversations_router)
