import logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.db_engine import sync_engine
from db.models.models import User

logger = logging.getLogger(__name__)


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(User)).scalar_one_or_none() is not None:
                logger.info("User already exists, skipping seeding")
                return
            logger.info("Seeding user")
            session.add(User(name="Alice"))
            session.commit()
