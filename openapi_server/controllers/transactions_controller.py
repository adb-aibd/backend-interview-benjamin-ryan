import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.fx_transaction import FxTransaction  # noqa: E501
from openapi_server.models.fx_transaction_request import FxTransactionRequest  # noqa: E501
from openapi_server.models.transaction_side import TransactionSide  # noqa: E501
from openapi_server import util


def create_transaction(body):  # noqa: E501
    """Record an FX transaction

    Records a foreign exchange transaction.  The transaction timestamp determines the transaction date used to look up the applicable daily exchange rate.  Exactly one of foreign_amount or base_amount must be supplied.  The applicable daily rate is captured as effective_rate so that later changes to daily rates do not affect the historical transaction.  # noqa: E501

    :param fx_transaction_request: 
    :type fx_transaction_request: dict | bytes

    :rtype: Union[FxTransaction, Tuple[FxTransaction, int], Tuple[FxTransaction, int, Dict[str, str]]
    """
    fx_transaction_request = body
    if flask.request.is_json:
        fx_transaction_request = FxTransactionRequest.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_transaction(transaction_id):  # noqa: E501
    """Get a recorded transaction

     # noqa: E501

    :param transaction_id: Internal transaction identifier.
    :type transaction_id: str

    :rtype: Union[FxTransaction, Tuple[FxTransaction, int], Tuple[FxTransaction, int, Dict[str, str]]
    """
    return 'do some magic!'


def list_transactions(_from=None, to=None, side=None, base_currency=None, quote_currency=None):  # noqa: E501
    """List recorded transactions

     # noqa: E501

    :param _from: Return transactions at or after this timestamp.
    :type _from: str
    :param to: Return transactions before or at this timestamp.
    :type to: str
    :param side: 
    :type side: dict | bytes
    :param base_currency: 
    :type base_currency: str
    :param quote_currency: 
    :type quote_currency: str

    :rtype: Union[List[FxTransaction], Tuple[List[FxTransaction], int], Tuple[List[FxTransaction], int, Dict[str, str]]
    """
    _from = util.deserialize_datetime(_from)
    to = util.deserialize_datetime(to)
    if flask.request.is_json:
        side =  TransactionSide.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'
