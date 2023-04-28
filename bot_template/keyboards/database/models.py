from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseMixin():
    def to_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }


class Callback(BaseMixin, Base):
    __tablename__ = "callbacks"
    id = Column(Integer, primary_key=True, unique=True)
    query = Column(String, nullable=False)
    original_query = Column(String, nullable=False)
    data = Column(String, nullable=True)
    die_time = Column(Integer, nullable=False)
