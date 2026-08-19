from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.db.models.currency import Currency
from app.db.models.exchange_rate import ExchangeRate, ExchangeRateSide
from app.services.currency_service import get_currencies_by_codes


class SameCurrencyError(Exception):
    pass


def _normalize_calculated_value(val: Decimal):
    """
    Quantizes calculated values (e.g. for inverse rates) to 10 decimal places
    for consistency with the DB.
    """
    return val.quantize(Decimal("0.0000000001"))


def post_exchange_rate(
    session: Session,
    rate_date: datetime,
    rate: Decimal,
    base_currency: Currency,
    quote_currency: Currency,
    side: ExchangeRateSide,
):
    # normalize pairing, base currency is always alphabetically first
    canonical_base, canonical_quote = sorted(
        (base_currency, quote_currency), key=lambda c: c.iso_code
    )

    is_flipped = canonical_base.iso_code != base_currency.iso_code
    canonical_rate = rate if not is_flipped else _normalize_calculated_value(1 / rate)
    canonical_side = (
        side
        if not is_flipped
        else (
            ExchangeRateSide.BUY
            if side == ExchangeRateSide.SELL
            else ExchangeRateSide.SELL
        )
    )

    exchange_rate = ExchangeRate(
        base_currency=canonical_base,
        quote_currency=canonical_quote,
        side=canonical_side,
        rate=canonical_rate,
        rate_date=rate_date,
    )

    session.add(exchange_rate)
    session.flush()

    return exchange_rate
