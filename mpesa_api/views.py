from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_creden import MpesaAccessToken, LipanaMpesaPpassword


def getAccessToken(request):
    consumer_key = 'swoZGI5VaiRUdoibxXOETKH0AbBwHFtY'
    consumer_secret = 'BEGvTOt9iI9aOmzH'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254707486233, 
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254707486233, 
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Ibrahim",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')