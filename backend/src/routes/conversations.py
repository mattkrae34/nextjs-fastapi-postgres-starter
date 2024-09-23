import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.conversations import ConversationCreate, ConversationRead, ConversationReadWithMessages
from schemas.messages import MessageCreate, MessageRead
from db.models.models import Conversation, Message
from db.db_engine import engine
from sqlalchemy import select
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ConversationRead], include_in_schema=False)
@router.get("", response_model=list[ConversationRead])
async def get_conversations():
    # TODO: get user_id from token / auth / upstream
    user_id = 1

    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(
                select(Conversation).where(Conversation.user_id == user_id)
            )
            conversations = result.scalars().all()
            if conversations is None:
                return []

            return [ConversationRead.model_validate(conversation) for conversation in conversations]


@router.get(
    "/{conversation_id}", response_model=ConversationReadWithMessages, include_in_schema=False
)
@router.get("/{conversation_id}", response_model=ConversationReadWithMessages)
async def get_conversation(conversation_id: int):
    # TODO: get user_id from token / auth / upstream
    user_id = 1

    try:
        async with AsyncSession(engine) as session:
            async with session.begin():
                query = (
                    select(Conversation)
                    .options(selectinload(Conversation.messages))
                    .where(Conversation.id == conversation_id and Conversation.user_id == user_id)
                )

                result = await session.execute(query)
                conversation_result = result.scalar_one_or_none()

                messages = [
                    MessageRead.model_validate(message) for message in conversation_result.messages
                ]
                return ConversationReadWithMessages(
                    id=conversation_result.id,
                    created_at=conversation_result.created_at,
                    updated_at=conversation_result.updated_at,
                    messages=messages,
                )
    except Exception as e:
        logger.error(f"Error getting conversation by id {conversation_id}: {e}")
        raise e


@router.post(
    "/", status_code=201, response_model=ConversationReadWithMessages, include_in_schema=False
)
@router.post("", status_code=201, response_model=ConversationReadWithMessages)
async def create_conversation(conversation_create: ConversationCreate):
    # TODO: get user_id from token / auth / upstream
    user_id = 1

    logger.info(
        f"Creating conversation for user {user_id} with content {conversation_create.content}"
    )

    async with AsyncSession(engine) as session:
        async with session.begin():
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            await session.flush()
            logger.info(f"Conversation created with id {conversation.id}")

            message = Message(
                conversation_id=conversation.id,
                content=conversation_create.content,
            )
            session.add(message)
            await session.flush()
            logger.info(f"Message created with id {message.id}")

            response = """
                Fusce semper massa viverra erat elementum, sit amet ultricies nunc pellentesque. Fusce egestas mi id lorem sagittis blandit. Nulla ipsum sapien, placerat sit amet consectetur eget, luctus eu justo. Curabitur vulputate sit amet augue et egestas. Morbi sollicitudin aliquam blandit. Aliquam erat volutpat. Donec mauris felis, pretium in mattis ut, volutpat at arcu. Praesent sodales, quam quis pulvinar suscipit, felis velit commodo enim, eget suscipit lectus orci ut erat. In scelerisque lacus et tortor faucibus vehicula.
            """

            message = Message(
                conversation_id=conversation.id,
                content=response,
            )

            session.add(message)
            await session.flush()
            logger.info(f"Message created with id {message.id}")

            query = (
                select(Conversation)
                .options(selectinload(Conversation.messages))
                .where(Conversation.id == conversation.id)
            )

            result = await session.execute(query)
            conversation_result = result.scalar_one_or_none()
            # TODO: figure out pydantic / sqlalchemy conversion sorcery
            messages = [
                MessageRead.model_validate(message) for message in conversation_result.messages
            ]
            return ConversationReadWithMessages(
                id=conversation_result.id,
                created_at=conversation_result.created_at,
                updated_at=conversation_result.updated_at,
                messages=messages,
            )


@router.post(
    "/{conversation_id}/messages",
    status_code=201,
    response_model=ConversationReadWithMessages,
    include_in_schema=False,
)
@router.post(
    "/{conversation_id}/messages", status_code=201, response_model=ConversationReadWithMessages
)
async def create_message(conversation_id: int, message_create: MessageCreate):
    # TODO: get user_id from token / auth / upstream
    user_id = 1

    async with AsyncSession(engine) as session:
        async with session.begin():
            query = (
                select(Conversation)
                .options(selectinload(Conversation.messages))
                .where(Conversation.id == conversation_id and Conversation.user_id == user_id)
            )

            result = await session.execute(query)
            conversation_result = result.scalar_one_or_none()

            if conversation_result is None:
                raise HTTPException(status_code=404, detail="Conversation not found")

            message = Message(
                conversation_id=conversation_id,
                content=message_create.content,
            )

            session.add(message)
            await session.flush()
            logger.info(f"Message created with id {message.id}")

            response = """
                Fusce semper massa viverra erat elementum, sit amet ultricies nunc pellentesque. Fusce egestas mi id lorem sagittis blandit. Nulla ipsum sapien, placerat sit amet consectetur eget, luctus eu justo. Curabitur vulputate sit amet augue et egestas. Morbi sollicitudin aliquam blandit. Aliquam erat volutpat. Donec mauris felis, pretium in mattis ut, volutpat at arcu. Praesent sodales, quam quis pulvinar suscipit, felis velit commodo enim, eget suscipit lectus orci ut erat. In scelerisque lacus et tortor faucibus vehicula.
            """

            message = Message(
                conversation_id=conversation_id,
                content=response,
            )

            session.add(message)
            await session.flush()
            logger.info(f"Message created with id {message.id}")

            await session.refresh(conversation_result)

            messages = [
                MessageRead.model_validate(message) for message in conversation_result.messages
            ]

            return ConversationReadWithMessages(
                id=conversation_result.id,
                created_at=conversation_result.created_at,
                updated_at=conversation_result.updated_at,
                messages=messages,
            )
