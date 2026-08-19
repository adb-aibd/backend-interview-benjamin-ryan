import flask
from decimal import Decimal
from typing import Dict
from typing import Tuple
from typing import Union

from app.services.currency_service import get_currencies_by_codes
from openapi_server.models.daily_rate import DailyRate  # noqa: E501
from openapi_server.models.daily_rate_update import DailyRateUpdate  # noqa: E501
from openapi_server.models.daily_rate_upsert import DailyRateUpsert  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.transaction_side import TransactionSide  # noqa: E501
from openapi_server import util

from app.db import SessionFactory
from app.db.models.exchange_rate import ExchangeRateSide
from app.services.exchange_rate_service import post_exchange_rate


def delete_rate(rate_date, base_currency, quote_currency, side):  # noqa: E501
    """Delete a daily exchange rate

     # noqa: E501

    :param rate_date:
    :type rate_date: str
    :param base_currency:
    :type base_currency: str
    :param quote_currency:
    :type quote_currency: str
    :param side:
    :type side: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    rate_date = util.deserialize_date(rate_date)
    if flask.request.is_json:
        side = TransactionSide.from_dict(flask.request.get_json())  # noqa: E501
    return None, 501


def get_rate(rate_date, base_currency, quote_currency, side):  # noqa: E501
    """Get a daily exchange rate

     # noqa: E501

    :param rate_date: 
    :type rate_date: str
    :param base_currency: 
    :type base_currency: str
    :param quote_currency: 
    :type quote_currency: str
    :param side: 
    :type side: dict | bytes

    :rtype: Union[DailyRate, Tuple[DailyRate, int], Tuple[DailyRate, int, Dict[str, str]]
    """
    rate_date = util.deserialize_date(rate_date)
    if flask.request.is_json:
        side =  TransactionSide.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def list_rates(rate_date=None, base_currency=None, quote_currency=None, side=None):  # noqa: E501
    """List daily exchange rates

     # noqa: E501

    :param rate_date: 
    :type rate_date: str
    :param base_currency: 
    :type base_currency: str
    :param quote_currency: 
    :type quote_currency: str
    :param side: 
    :type side: dict | bytes

    :rtype: Union[List[DailyRate], Tuple[List[DailyRate], int], Tuple[List[DailyRate], int, Dict[str, str]]
    """
    rate_date = util.deserialize_date(rate_date)
    if flask.request.is_json:
        side =  TransactionSide.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_rate(rate_date, base_currency, quote_currency, side, body):  # noqa: E501
    """Replace a daily exchange rate

     # noqa: E501

    :param rate_date: 
    :type rate_date: str
    :param base_currency: 
    :type base_currency: str
    :param quote_currency: 
    :type quote_currency: str
    :param side: 
    :type side: dict | bytes
    :param daily_rate_update: 
    :type daily_rate_update: dict | bytes

    :rtype: Union[DailyRate, Tuple[DailyRate, int], Tuple[DailyRate, int, Dict[str, str]]
    """
    rate_date = util.deserialize_date(rate_date)
    if flask.request.is_json:
        side =  TransactionSide.from_dict(flask.request.get_json())  # noqa: E501
    daily_rate_update = body
    if flask.request.is_json:
        daily_rate_update = DailyRateUpdate.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_rate(body):  # noqa: E501
    """Create or update a daily exchange rate

    Creates a daily rate or updates the existing rate for the same rate date, currency pair, and transaction side.  # noqa: E501

    Currency pairs are normalized to use the currency code that comes alphabetically first as the base rate (e.g. posting "USD/EUR BUY rate" is saved as a "EUR/USD SELL 1/rate").
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
