import unittest

from flask import json

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.fx_transaction import FxTransaction  # noqa: E501
from openapi_server.models.fx_transaction_request import FxTransactionRequest  # noqa: E501
from openapi_server.models.transaction_side import TransactionSide  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTransactionsController(BaseTestCase):
    """TransactionsController integration test stubs"""

    def test_create_transaction(self):
        """Test case for create_transaction

        Record an FX transaction
        """
        fx_transaction_request = {"timestamp":"2026-02-02T10:15:00+08:00","base_currency":"PHP","quote_currency":"PHP","side":"BUY","foreign_amount":"1000.00"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/transactions',
            method='POST',
            headers=headers,
            data=json.dumps(fx_transaction_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_transaction(self):
        """Test case for get_transaction

        Get a recorded transaction
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/transactions/{transaction_id}'.format(transaction_id='TXN-20260202-000001'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_transactions(self):
        """Test case for list_transactions

        List recorded transactions
        """
        query_string = [('from', '2013-10-20T19:20:30+01:00'),
                        ('to', '2013-10-20T19:20:30+01:00'),
                        ('side', openapi_server.TransactionSide()),
                        ('base_currency', 'base_currency_example'),
                        ('quote_currency', 'quote_currency_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/transactions',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
