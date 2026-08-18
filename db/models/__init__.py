from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SAEnum,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TransactionSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class RateSnapshot(Base):
    """
    Immutable snapshot of an exchange rate that became effective at a
    particular point in time.

    A new row is created whenever the store changes its rate.

    To find the rate applicable to a transaction:

        latest snapshot where
            base_currency   = transaction.base_currency
            quote_currency  = transaction.quote_currency
            side            = transaction.side
            effective_at    <= transaction.timestamp

    ordered by effective_at DESC.
    """

    __tablename__ = "rate_snapshots"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    effective_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    base_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    quote_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    side: Mapped[TransactionSide] = mapped_column(
        SAEnum(
            TransactionSide,
            name="transaction_side",
            native_enum=False,
            length=4,
        ),
        nullable=False,
    )

    # Exact decimal exchange rate.
    #
    # Example:
    #   1.3550
    #
    # Stored as NUMERIC rather than FLOAT/DOUBLE.
    rate: Mapped[Decimal] = mapped_column(
        Numeric(20, 10),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "effective_at",
            "base_currency",
            "quote_currency",
            "side",
            name="uq_rate_snapshot_effective_at_pair_side",
        ),
    )


class FxTransaction(Base):
    __tablename__ = "fx_transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )

    transaction_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    base_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    quote_currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    side: Mapped[TransactionSide] = mapped_column(
        SAEnum(
            TransactionSide,
            name="transaction_side",
            native_enum=False,
            length=4,
        ),
        nullable=False,
    )

    # Amounts are stored as integer minor units.
    #
    # Example:
    #   API: "1000.00"
    #   DB:  100000
    #
    # The scale is determined by the currency.
    foreign_amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    base_amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    # Snapshot of the exact rate used by this transaction.
    effective_rate: Mapped[Decimal] = mapped_column(
        Numeric(20, 10),
        nullable=False,
    )

    fee_amount: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )

    rounding_adjustment: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
