from django.shortcuts import render
from django.http import request
from django.views.decorators.csrf import csrf_exempt


import sys
import urllib.parse
import requests

# Create your views here.

@csrf_exempt
def ipn_listender(request):

    field_to_check = ['pl_receiver_email', 'pl_custom', 'pl_handling_amount', 'pl_mc_currency', 'pl_payment_status']

    VERIFY_URL_PROD = 'https://www.paypal.com/cgi-bin/webscr'
    # VERIFY_URL_TEST = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
    VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

    # Switch as appropriate
    VERIFY_URL = VERIFY_URL_TEST

    # CGI preamble
    print("content-type: text/plain")
    print()

    # for item in request.POST:
    #     print(item)
    #     print(request.POST[item])
    #     print()

    param_str = request.body
    print(param_str)
    params = urllib.parse.parse_qsl(param_str)


    # Add '_notify-validate' parameter
    params.append(('cmd', '_notify-validate'))

    # Post back to PayPal for validation
    headers = {'content-type': 'application/x-www-form-urlencoded', 'host': 'www.paypal.com'}
    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    r.raise_for_status()

    # Check return message and take action as needed
    if r.text == 'VERIFIED':
        custom = request.POST.get('custom')

        receiver_email = request.POST.get('receiver_email')
        handling_amount = request.POST.get('handling_amount')
        mc_currency = request.POST.get('mc_currency')
        payment_status = request.POST.get('payment_status')

        print(custom)
        print(receiver_email)
        print(handling_amount)
        print(mc_currency)
        print(payment_status)

    elif r.text == 'INVALID':
        pass
    else:
        pass
    print(r.text)



if __name__ == '__main__':
    ipn_listender(request)