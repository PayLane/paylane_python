# -*- coding: utf-8 -*-

import logging
import requests
import simplejson

from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)


class PayLaneRestClient(object):
    """Client library for Paylane REST Server.
    More info at: http://devzone.paylane.com    
    """

    API_URL = 'https://direct.paylane.com/rest/'
    CONTENT_TYPE = 'application/json'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.success = None

    def card_sale(self, params):
        """Performs card sale

        @param params: Sale params
        @return: dict
        """
        return self._call('cards/sale', 'post', params)

    def card_sale_by_token(self, params):
        """Performs card sale by token

        @param params: Sale params
        @return: dict
        """
        return self._call('cards/saleByToken', 'post', params)

    def card_authorization(self, params):
        """Card authorization

        @param params: Authorization params
        @return: dict
        """
        return self._call('cards/authorization', 'post', params)

    def card_authorization_by_token(self, params):
        """Card authorization by token

        @param params: Authorization params
        @return: dict
        """
        return self._call('cards/authorizationByToken', 'post', params)

    def paypal_authorization(self, params):
        """PayPal authorization

        @param params:
        @return: dict
        """
        return self._call('paypal/authorization', 'post', params)

    def capture_authorization(self, params):
        """Performs capture from authorized card

        @param params: Capture authorization params
        @return: dict
        """
        return self._call('authorizations/capture', 'post', params)

    def close_authorization(self, params):
        """Performs closing of card authorization, basing on authorization
        card ID

        @param params: Close authorization params
        @return: dict
        """
        return self._call('authorizations/close', 'post', params)

    def refund(self, params):
        """Performs refund

        @param params: Refund params
        @return: dict
        """
        return self._call('refunds', 'post', params)

    def get_sale_info(self, params):
        """Get sale info

        @param params: Get sale info params
        @return: dict
        """
        return self._call('sales/info', 'get', params)

    def get_authorization_info(self, params):
        """Get sale info

        @param params: Get sale info params
        @return: dict
        """
        return self._call('authorizations/info', 'get', params)

    def check_sale_status(self, params):
        """Performs sale status check

        @param params: Check sale status
        @return: dict
        """
        return self._call('sales/status', 'get', params)

    def direct_debit_sale(self, params):
        """Direct debit sale

        @param params: Direct debit params
        @return: dict
        """
        return self._call('directdebits/sale', 'post', params)

    def sofort_sale(self, params):
        """Sofort sale

        @param params: Sofort params
        @return: dict
        """
        return self._call('sofort/sale', 'post', params)

    def ideal_sale(self, params):
        """iDeal sale

        @param params: Ideal transaction params
        @return: dict
        """
        return self._call('ideal/sale', 'post', params)

    def ideal_bank_codes(self):
        """iDeal bank list

        @return: dict
        """
        return self._call('ideal/bankcodes', 'get')


    def bank_transfer_sale(self, params):
        """Bank transfer sale

        @param params: Bank transfer sale params
        @return: dict
        """
        return self._call('banktransfers/sale', 'post', params)

    def paypal_sale(self, params):
        """PayPal sale

        @param params: Paypal sale params
        @return: dict
        """
        return self._call('paypal/sale', 'post', params)

    def paypal_stop_recurring(self, params):
        """Cancels Paypal recurring profile

        @param params: Paypal params
        @return dict
        """
        return self._call('paypal/stopRecurring', 'post', params)

    def resale_by_sale(self, params):
        """ Performs resale by sale ID

        @param params: Resale by sale params
        @return: dict
        """
        return self._call('resales/sale', 'post', params)

    def resale_by_authorization(self, params):
        """Performs resale by authorization ID

        @param params: Resale by authorization params
        @return: dict
        """
        return self._call('resales/authorization', 'post', params)

    def check_card_3d_secure(self, params):
        """Checks if a card is enrolled in the 3D-Secure program.

        @param params: Check card 3-D Secure params
        @return: dict
        """
        return self._call('3DSecure/checkCard', 'get', params)

    def check_card_3d_secure_by_token(self, params):
        """Checks if a card is enrolled in the 3D-Secure program, based on the card's token.

        @param params: Check card 3-D Secure params
        @return: dict
        """
        return self._call('3DSecure/checkCardByToken', 'get', params)

    def sale_by_3d_secure_authorization(self, params):
        """Performs sale by ID 3-D Secure authorization

        @param params: Sale by 3-D Secure authorization params
        @return: dict
        """
        return self._call('3DSecure/authSale', 'post', params)

    def check_card(self, params):
        """Perform check card

        @param params: Check card params
        @return: dict
        """
        return self._call('cards/check', 'get', params)

    def check_card_by_token(self, params):
        """Perform check card by token

        @param params: Check card params
        @return: dict
        """
        return self._call('cards/checkByToken', 'get', params)

    def is_success(self):
        """Request state getter

        @return: bool
        """
        return self.success

    def _call(self, call_name, call_method, params={}):
        """Method responsible for preparing, setting state, pushing data to
        REST server and returning answer

        @param call_name: REST call name
        @param call_method: HTTP verb (get, post, put, etc.)
        @param params: dict with params to send
        @return: dict
        """
        call_method = call_method.upper()
        call_url = '%s%s' % (self.API_URL, call_name)
        headers = {'content-type': self.CONTENT_TYPE}
        auth = HTTPBasicAuth(self.username, self.password)
        data = simplejson.dumps(params)

        response = requests.request(method=call_method, url=call_url,
            data=data, headers=headers, auth=auth, verify=True)

        self._handle_http_error(response)
        response_data = response.json()
        self._handle_response_error(response_data)
        return response_data

    def _handle_http_error(self, response):
        """Handle http error

        @param response: requests.models.Response for HTTP request
        @raise requests.exceptions.HTTPError: if response status code != 200
        """
        response.raise_for_status()

    def _handle_response_error(self, response_data):
        """Set state depending on response (success or failure)

        @param response_data: dict returned by REST server
        """
        if response_data.get('success') == True:
            self.success = True
        else:
            self.success = False
