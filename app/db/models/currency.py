from sqlalchemy import CheckConstraint, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


# TODO: Populate from the ISO 4217 authoritative currency list? Or use some service?
class Currency(Base):
    __tablename__: str = "currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    iso_code: Mapped[str] = mapped_column(String(3), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    minor_units: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("iso_code", name="uq_currency_iso_code"),
        CheckConstraint(
            "iso_code ~ '^[A-Z]{3}$'",
            name="ck_currency_iso_code_format",
        ),
        CheckConstraint(
            "length(trim(name)) > 0",
            name="ck_currency_name_not_empty",
        ),
        CheckConstraint(
            "minor_units >= 0",
            name="ck_currency_minor_units_not_negative",
        ),
    )
