from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    slug: Mapped[str] = mapped_column(primary_key=True)
    long_url: Mapped[str]