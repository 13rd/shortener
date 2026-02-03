from datetime import datetime, timedelta, UTC
from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass


class ShortUrl(Base):
    __tablename__ = 'short_urls'

    slug: Mapped[str] = mapped_column(primary_key=True)
    long_url: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(UTC)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        Index('idx_expires_at', 'expires_at'),
        )