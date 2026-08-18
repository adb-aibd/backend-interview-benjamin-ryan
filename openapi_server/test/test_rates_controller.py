import unittest

from flask import json

from openapi_server.models.daily_rate import DailyRate  # noqa: E501
from openapi_server.models.daily_rate_update import DailyRateUpdate  # noqa: E501
from openapi_server.models.daily_rate_upsert import DailyRateUpsert  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.transaction_side import TransactionSide  # noqa: E501
from openapi_server.test import BaseTestCase


class TestRatesController(BaseTestCase):
    """RatesController integration test stubs"""

    def test_delete_rate(self):
        """Test case for delete_rate

        Delete a daily exchange rate
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/rates/{rate_date}/{base_currency}/{quote_currency}/{side}'.format(rate_date='2026-02-02', base_currency='PHP', quote_currency='USD', side=openapi_server.TransactionSide()),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_rate(self):
        """Test case for get_rate

        Get a daily exchange rate
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/rates/{rate_date}/{base_currency}/{quote_currency}/{side}'.format(rate_date='2026-02-02', base_currency='PHP', quote_currency='USD', side=openapi_server.TransactionSide()),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_rates(self):
        """Test case for list_rates

        List daily exchange rates
        """
        query_string = [('rate_date', '2013-10-20'),
                        ('base_currency', 'base_currency_example'),
                        ('quote_currency', 'quote_currency_example'),
                        ('side', openapi_server.TransactionSide())]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/rates',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_rate(self):
        """Test case for update_rate

        Replace a daily exchange rate
        """
        daily_rate_update = {"rate":"1000.00"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/rates/{rate_date}/{base_currency}/{quote_currency}/{side}'.format(rate_date='2026-02-02', base_currency='PHP', quote_currency='USD', side=openapi_server.TransactionSide()),
            method='PUT',
            headers=headers,
            data=json.dumps(daily_rate_update),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upsert_rate(self):
        """Test case for upsert_rate

        Create or update a daily exchange rate
        """
        daily_rate_upsert = {"rate_date":"2026-02-02","base_currency":"PHP","quote_currency":"PHP","side":"BUY","rate":"1000.00"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/rates',
            method='POST',
            headers=headers,
            data=json.dumps(daily_rate_upsert),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
