from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.currency import Currency


class CurrencyNotFoundError(Exception):
    pass


# batch fetch to reduce trips
def get_currencies_by_codes(
    session: Session, currency_codes: set[str]
) -> dict[str, Currency]:
    """Get currencies by ISO code, raising if any are missing"""
    result = session.execute(
        select(Currency).where(Currency.iso_code.in_(currency_codes))
    )

    fetched_currencies = {currency.iso_code: currency for currency in result.scalars()}

    missing_currency_codes = currency_codes - fetched_currencies.keys()

    if missing_currency_codes:
        raise CurrencyNotFoundError(missing_currency_codes)

    return fetched_currencies
