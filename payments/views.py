from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


from .models import Payment, Pricing, TransactionPaypal
from events.models import Event


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

    # Send empty response to paypal
    # r_initial = requests.post(VERIFY_URL, headers={'Status': '200'})
    # r_initial.raise_for_status()
    # print(f'initial reply: {r_initial}')


    # Add '_notify-validate' parameter
    params.append(('cmd', '_notify-validate'))

    # Post back to PayPal for validation
    headers = {'content-type': 'application/x-www-form-urlencoded', 'host': 'www.paypal.com'}
    r = requests.post(VERIFY_URL, params=params, headers=headers, verify=True)
    r.raise_for_status()


    # Get all variables needed to verify and record into our transaction table
    try:
        # order are eventID, userID, paymentID, pricingID
        custom = request.POST.get('custom').split(',')
        eventID = custom[0]
        userID = custom[1]
        paymentID = custom[2]
        pricingID = custom[3]
    except IndexError:
        print("Error: custom information is missing or tempered with")
        return "error or 404 or whatever page?"

    # Get my custom details to verify against database also
    receiver_email = request.POST.get('receiver_email').replace('%40', '@')
    handling_amount = request.POST.get('handling_amount')
    mc_gross = request.POST.get('mc_gross')
    mc_currency = request.POST.get('mc_currency')
    payment_status = request.POST.get('payment_status')

    cur_pricing = Pricing.objects.get(pk=pricingID)
    cur_pricing_amount = cur_pricing.amount
    cur_payment = Payment.objects.get(pk=paymentID)
    cur_event = Event.objects.get(pk=eventID)

    # Check return message and take action as needed
    if r.text == 'VERIFIED':
    #TODO: Check correct payment field from IPN.
        #TODO: Check if GBP is returned corrected and if from other currency if there's issue with numbers?

        # Check to see if payment IPN details are correct here.
        if receiver_email == "JinPark.Han-facilitator@gmail.com":
            print("receiver email ok")
            if payment_status=='Completed':
                print(f"payment_status: {payment_status}")
                if mc_currency == 'GBP': #TODO: for dev purpose USD
                    print(f"mc_currency: {mc_currency}")
                    print(f"pricingID: {pricingID}")
                    if cur_pricing_amount == mc_gross:
                        print("cur_pricing_amount == mc_gross")
                        print(f"   {cur_pricing_amount} == {mc_gross}")
                        if cur_payment.id == cur_pricing.payment_id:
                            print("cur_payment.id == cur_pricing.payment_id")
                            if cur_payment.event_id == cur_event.id:
                                print("cur_payment.event_id == cur_event.id")
                                # After all check add info to database?
                                TransactionPaypal.objects.create(
                                    pl_receiver_email = receiver_email,
                                    # pl_receiver_id
                                    pl_custom = custom,
                                    pl_mc_gross = mc_gross,
                                    pl_mc_currency = mc_currency,
                                    pl_payment_status = payment_status,
                                    event = cur_event,
                                    buyer = User.objects.get(pk=userID),
                                    # paymentID = ,
                                    pricing = cur_pricing,
                                    status = 'verified',
                                )
                                print("All data match database. Saved to DB and transaction COMPLETE and VERIFIED")
                            else:
                                print("error: cur_payment.event_id == cur_event.id")
                        else:
                            print("error: cur_payment.id == cur_pricing.payment_id")
                    else:
                        print("error: cur_pricing_amount == handling_amount")
                        print(f"error: {cur_pricing_amount} == {handling_amount}")
                else:
                    print(f"error: mc_currency: {mc_currency}")
            else:
                print(f"error: payment_status: {payment_status}")
        else:
            print(f"wrong receiver email {receiver_email}")


    elif r.text == 'INVALID':
        TransactionPaypal.objects.create(
            pl_receiver_email = receiver_email,
            # pl_receiver_id
            pl_custom = custom,
            pl_mc_gross = mc_gross,
            pl_mc_currency = mc_currency,
            pl_payment_status = payment_status,
            event = cur_event,
            buyer = User.objects.get(pk=userID),
            # paymentID = ,
            pricing = cur_pricing,
            status = 'invalid',
        )
    else:
        pass
    print(r.text)
    #TODO: This should be first in process.
    return HttpResponse('')