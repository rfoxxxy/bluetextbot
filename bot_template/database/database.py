import html
from typing import List

from sqlalchemy import exc, select

from bot_template import db
from bot_template.database import exceptions
from bot_template.database.models import User


async def register_user(event, session: db.Session) -> User:
    try:
        user = (await
                session.execute(select(User).filter_by(id=event.from_user.id)
                                )).unique().scalar_one()
    except exc.NoResultFound:
        user = await User().create(session,
                                   id=event.from_user.id,
                                   username=event.from_user.username,
                                   name=html.escape(event.from_user.full_name))
        return user
    raise exceptions.RegistrationError(
        f"user {event.from_user.id} already registered")


async def get_user(user_id: int, session: db.Session) -> User:
    user: User = None
    try:
        user = (await session.execute(select(User).filter_by(id=user_id)
                                      )).unique().scalar_one()
    except exc.NoResultFound:
        pass
    if not user:
        raise exceptions.NotFoundError(f"user {user_id} not found")
    return user


async def get_all_users(session: db.Session) -> List[User]:
    users = (await session.execute(select(User))).unique().scalars().all()
    return users
