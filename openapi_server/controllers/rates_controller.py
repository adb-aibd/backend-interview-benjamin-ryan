import flask
from datetime import date, datetime
from decimal import Decimal
from typing import Dict
from typing import Tuple
from typing import Union

from app.services.currency_service import get_currencies_by_codes
from openapi_server.models.daily_rate import DailyRate  # noqa: E501
from openapi_server.models.daily_rate_update import DailyRateUpdate  # noqa: E501
from openapi_server.models.daily_rate_upsert import DailyRateUpsert  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.exchange_rate import ExchangeRate
from openapi_server.models.transaction_side import TransactionSide  # noqa: E501
from openapi_server import util

from app.db import SessionFactory
from app.db.models.exchange_rate import ExchangeRateSide
from app.services.exchange_rate_service import get_exchange_rate, post_exchange_rate


def get_rate(base_currency, quote_currency, side, rate_date=None):  # noqa: E501
    """Get a daily exchange rate

     # noqa: E501

    :param base_currency:
    :type base_currency: str
    :param quote_currency:
    :type quote_currency: str
    :param side:
    :type side: dict | bytes
    :param rate_date: Filters the rate by the specified date. When specified, the latest rate from that date is returned. If there is no posted rate for the specified date, returns the latest rate.  Must be less than or equal to today&#39;s date (UTC), and greater than UNIX epoch (i.e. 1970-01-01)
    :type rate_date: str

    :rtype: Union[DailyRate, Tuple[DailyRate, int], Tuple[DailyRate, int, Dict[str, str]]
    """
    # TODO: Generalize date validation
    now = datetime.now()
    if rate_date is None:
        rate_date = now

    try:
        validated_rate_date = datetime.strptime(rate_date, "%Y-%m-%d")
    except ValueError:
        return {"code": "INVALID_DATE", "message": "rateDate is not a valid date"}, 400

    if validated_rate_date.date() > now.date():
        return {"code": "INVALID_DATE", "message": "rateDate is in the future"}, 400

    if base_currency == quote_currency:
        return {
            "code": "SAME_CURRENCY",
            "message": "Base and quote currencies cannot be the same.",
        }, 400

    with SessionFactory() as session, session.begin():
        currencies = get_currencies_by_codes(
            session=session,
            currency_codes={
                base_currency,
                quote_currency,
            },
        )

        exchange_rate = get_exchange_rate(
            session=session,
            rate_date=validated_rate_date,
            base_currency=currencies[base_currency],
            quote_currency=currencies[quote_currency],
            side=ExchangeRateSide(side),
        )

        return (
            (
                DailyRate(
                    rate_date=exchange_rate.rate_date.date(),
                    rate=exchange_rate.rate,
                    base_currency=exchange_rate.base_currency.iso_code,
                    quote_currency=exchange_rate.quote_currency.iso_code,
                    side=exchange_rate.side.value,
                ),
                200,
            )
            if exchange_rate is not None
            else (
                {
                    "code": "DAILY_RATE_NOT_FOUND",
                    "message": "Daily exchange rate not found.",
                },
                404,
            )
        )


def post_rate(body):  # noqa: E501
    """Create an exchange rate

    Creates an exchange rate for the specified rate date, currency pair, and transaction side.  Currency pairs are normalized to use the currency code that comes alphabetically first as the base rate (e.g. posting \&quot;USD/EUR BUY rate\&quot; is saved as a \&quot;EUR/USD SELL 1/rate\&quot;).  # noqa: E501

    :param daily_rate_upsert:
    :type daily_rate_upsert: dict | bytes

    :rtype: Union[DailyRate, Tuple[DailyRate, int], Tuple[DailyRate, int, Dict[str, str]]
    """
    daily_rate_upsert = body
    if flask.request.is_json:
        daily_rate_upsert = DailyRateUpsert.from_dict(flask.request.get_json())  # noqa: E501

        with SessionFactory() as session, session.begin():
            base_currency_code = daily_rate_upsert.base_currency
            quote_currency_code = daily_rate_upsert.quote_currency

            if base_currency_code == quote_currency_code:
                return {
                    "code": "SAME_CURRENCY",
                    "message": "Base and quote currencies cannot be the same.",
                }

            currencies = get_currencies_by_codes(
                session=session,
                currency_codes={
                    base_currency_code,
                    quote_currency_code,
                },
            )

            exchange_rate = post_exchange_rate(
                session=session,
                rate_date=daily_rate_upsert.rate_date,
                rate=Decimal(daily_rate_upsert.rate),
                base_currency=currencies[base_currency_code],
                quote_currency=currencies[quote_currency_code],
                side=ExchangeRateSide(daily_rate_upsert.side),
            )

            return DailyRate(
                rate_date=exchange_rate.rate_date,
                rate=exchange_rate.rate,
                base_currency=exchange_rate.base_currency.iso_code,
                quote_currency=exchange_rate.quote_currency.iso_code,
                side=exchange_rate.side.value,
            ), 201
    return None, 400
