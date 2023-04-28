from sqlalchemy import BigInteger, Boolean, Column, String

from bot_template import db
from bot_template.database.utils.mixins import BaseMixin


class User(BaseMixin, db.Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    username = Column(String(64), nullable=True)
    name = Column(String, nullable=True)
    active = Column(Boolean, default=True)
