from sqlalchemy import inspect

from bot_template import db


class BaseMixin():
    @classmethod
    async def create(cls, session: db.Session = None, **kwargs):
        if not session:
            session = db.Session()
        _obj = cls(**kwargs)
        session.add(_obj)
        await session.commit()
        return _obj

    def to_dict(self) -> dict:
        """Get object as dict

        Returns:
            dict: object representation
        """
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
        }
