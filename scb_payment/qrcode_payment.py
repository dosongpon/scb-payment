"""
A libraly that provides a python interface to SCB Payment API
"""
import json

from .authorization import Authorization
from .business_code import BusinessCode
from .decorators import check_in_kwargs
from .error import SCBPaymentError
from .qr_type import QRType
from .request import basic_request


class QRCodePayment(Authorization):

    @check_in_kwargs(["amount", "ref1", "ref2", "ref3"])
    def gererate_qr_30(self, amount=None, ref1=None, ref2=None, ref3=None):
        url = self._get_path("PAYMENT_QRCODE_PATH")

        payload = {}
        payload["qrType"] = QRType.QR_30
        payload["amount"] = amount
        payload["ppType"] = "BILLERID"
        payload["ppId"] = self.biller
        payload["ref1"] = ref1
        payload["ref2"] = ref2
        payload["ref3"] = ref3
        payload = json.dumps(payload)

        response = basic_request('POST', url, headers=self._get_headers(), payload=payload)

        if response['status']['code'] != BusinessCode.SUCCESS:
            raise SCBPaymentError("{0} {1}".format(response['status']['code'], response['status']['description']))

        return response['data']

    @check_in_kwargs(["amount", "invoice"])
    def gererate_qr_cs(self, amount=None, invoice=None, description="", expiry_time=60, user_definded=""):
        url = self._get_path("PAYMENT_QRCODE_PATH")

        payload = {}
        payload["qrType"] = QRType.QR_CS
        payload["amount"] = amount
        payload["csExtExpiryTime"] = expiry_time
        payload["csNote"] = description
        payload["csUserDefined"] = user_definded
        payload["invoice"] = invoice
        payload["merchantId"] = self.merchant
        payload["terminalId"] = self.terminal
        payload = json.dumps(payload)

        response = basic_request('POST', url, headers=self._get_headers(), payload=payload)

        if response['status']['code'] != BusinessCode.SUCCESS:
            raise SCBPaymentError("{0} {1}".format(response['status']['code'], response['status']['description']))

        return response['data']

    @check_in_kwargs(["amount", "invoice", "ref1", "ref2", "ref3"])
    def gererate_qr_30_qr_cs(self, amount=None, invoice=None, description="", expiry_time=60, user_definded="", ref1=None, ref2=None, ref3=None):
        url = self._get_path("PAYMENT_QRCODE_PATH")

        payload = {}
        payload["qrType"] = QRType.QR_30_QR_CS
        payload["amount"] = amount
        payload["ppType"] = "BILLERID"
        payload["ppId"] = self.biller
        payload["ref1"] = ref1
        payload["ref2"] = ref2
        payload["ref3"] = ref3
        payload["csExtExpiryTime"] = expiry_time
        payload["csNote"] = description
        payload["csUserDefined"] = user_definded
        payload["invoice"] = invoice
        payload["merchantId"] = self.merchant
        payload["terminalId"] = self.terminal
        payload = json.dumps(payload)

        response = basic_request('POST', url, headers=self._get_headers(), payload=payload)

        if response['status']['code'] != BusinessCode.SUCCESS:
            raise SCBPaymentError("{0} {1}".format(response['status']['code'], response['status']['description']))

        return response['data']
