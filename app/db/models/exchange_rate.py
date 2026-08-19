from datetime import date, datetime
from decimal import Decimal
from enum import Enum as EnumType

from sqlalchemy import CheckConstraint, Date, DateTime, Enum, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.models.currency import Currency


class ExchangeRateSide(EnumType):
    """
    Defines the semantics of the rate.

    If BUY, foreign_currency = base_currency * rate
    If SELL, base_currency = foreign_currency / rate
    """

    BUY = "BUY"
    SELL = "SELL"


class ExchangeRate(Base):
    __tablename__: str = "exchange_rates"

    id: Mapped[int] = mapped_column(primary_key=True)

    """Actual insertion time, used for ordering when querying"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    """User-defined date"""
    rate_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
    quote_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
    side: Mapped[ExchangeRateSide] = mapped_column(
        Enum(ExchangeRateSide), nullable=False
    )

    rate: Mapped[Decimal] = mapped_column(
        Numeric(20, 10),
        nullable=False,
    )

    base_currency: Mapped[Currency] = relationship(
        foreign_keys=[base_currency_id],
    )

    quote_currency: Mapped[Currency] = relationship(
        foreign_keys=[quote_currency_id],
    )

    __table_args__ = (
        CheckConstraint(
            "base_currency_id <> quote_currency_id",
            name="ck_exchange_rate_different_currencies",
        ),
        CheckConstraint(
            "rate > 0",
            name="ck_exchange_rate_positive",
        ),
    )
