import datetime
import re

from sqlalchemy import Column, DateTime, BigInteger
from sqlalchemy.ext.declarative import declared_attr

from database import Base


class Model(Base):
    __abstract__ = True

    id = Column(
        BigInteger,
        primary_key=True
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return re.sub('(?!^)([A-Z]+)', r'_\1', cls.__name__).lower()
