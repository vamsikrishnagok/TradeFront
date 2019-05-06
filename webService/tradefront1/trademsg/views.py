from django.shortcuts import render,redirect
from .models import TradeMessage,TradeMessageHFloat
from django.urls import reverse
from django.contrib.auth import views as auth_views
from .models import APIINFO
import logging
from kiteconnect import KiteConnect
import requests

from datetime import datetime
import csv
import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)
import os



apiKey = None
accessToken = None
#

kite = None
# KiteConnect(api_key=apiKey)


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

# kite.set_access_token(accessToken)


# Create your views here. Question.objects.order_by('-pub_date')[:5]

from django.http import HttpResponse,JsonResponse


def how_many_seconds_until_midnight():
    """Get the number of seconds until midnight."""
    n = datetime.now()
    n.hour
    return ((24 - n.hour - 1) * 60 * 60) + ((60 - n.minute - 1) * 60) + (60 - n.second)

@csrf_exempt
@login_required
def index(request):


    try:
        p = APIINFO.objects.latest('id')
        print(datetime.now())
        return render(request, 'trademsg/index.html',context={"data":p})
    except:
        return redirect(reverse('trademsg:set_access_token'))

@csrf_exempt
@login_required
def pending_orders(request):

    p = APIINFO.objects.latest('id')

    apiKey = p.api_key
    accessToken = p.api_token
    kite = KiteConnect(api_key=apiKey)
    kite.set_access_token(accessToken)



    if request.method == "POST":
        KiteConnect.cancel_order(kite,request.POST["var"],request.POST["oid"])



    kite.orders()



    print(datetime.now())
    return render(request, 'trademsg/pending_orders.html', context={"orders": kite.orders()})







@csrf_exempt
@login_required
def trademsglf(request):
    return render(request,'trademsg/trademsglive.html')

@csrf_exempt
@login_required
def trademsglfsql(request):
    q = TradeMessage.objects.order_by('-date_time')[:100]
    return render(request, 'trademsg/trademsg.html',context = {"data":q})

@csrf_exempt
@login_required
def trademsghfsql(request):
    q = TradeMessageHFloat.objects.order_by('-date_time')[:100]
    return render(request, 'trademsg/trademsg.html',context = {"data":q})




@csrf_exempt
@login_required
def set_access_token(request):

    apii_key = 'l5x8ay13aegnq946'

    if request.method == "POST":


        accessToken = request.POST["access_token"]

        if "order_type" in request.POST:

            OT = request.POST["order_type"]
        else:
            OT = "SL"

        if "script_exp" in request.POST:
            se = int(request.POST["script_exp"])
        else:
            se = 1

        if "cup" in request.POST:
            cp = int(request.POST["cup"])
        else:
            cp = 1





        p = APIINFO(no=1, api_key=apii_key, api_token=request.POST["access_token"],
                    dattime=datetime.now(),order_type=OT,script_exposure=se,cushion_price=cp)
        p.save()
        return redirect(reverse('trademsg:index'))

    else:
        try:
            p = APIINFO.objects.latest('id')
            kite = KiteConnect(api_key=apii_key)
            r = requests.get(kite.login_url())
            return render(request, 'trademsg/set_access.html', context={"url": kite.login_url(), 'data': r.text,'dd':p})


        except:

            kite = KiteConnect(api_key=apii_key)
            r = requests.get(kite.login_url())
            return render(request, 'trademsg/set_access.html', context={"url": kite.login_url(), 'data': r.text})



@csrf_exempt
@login_required
def momo(request):


    return render(request, 'trademsg/momo.html')


@csrf_exempt
@login_required
def momo_high(request):


    return render(request, 'trademsg/momo_high.html')


@csrf_exempt
@login_required
def inter_report(request):


    return render(request, 'trademsg/report.html')

@csrf_exempt
@login_required
def inter_report_high(request):


    return render(request, 'trademsg/report_high.html')

@csrf_exempt
@login_required
def trade_high(request):


    return render(request, 'trademsg/trade_high.html')




@api_view(['GET', 'POST'])
@csrf_exempt
def buy(request):

    p = APIINFO.objects.latest('id')

    apiKey = p.api_key
    accessToken = p.api_token
    kite = KiteConnect(api_key=apiKey)
    kite.set_access_token(accessToken)

    r = requests.get(''.join(
        ["https://api.kite.trade/instruments/NSE/", request.POST["script"], "?api_key=", apiKey, '&access_token=',
         accessToken]))

    print(''.join(
        ["https://api.kite.trade/instruments/NSE/", request.POST["script"], "?api_key=", apiKey, '&access_token=',
         accessToken]))

    # r = requests.get("https://api.kite.trade/instruments/MCX/SILVERMIC18AUGFUT?api_key=l5x8ay13aegnq946&access_token=5978ylw21tvnnvs3jallyt9r98yw6zbj")
    v = json.loads(r.text)

    print(v)
    print(p.order_type)

    trigPrice = v["data"]["depth"]["sell"][0]["price"] + 0.20
    Price = trigPrice + (trigPrice * (p.cushion_price/100))
    script_exp = int(round(p.script_exposure / v["data"]["depth"]["sell"][0]["price"]))

    not_mis = False

    with open(''.join([dir_path,"/mis_blocked.csv"])) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(str(row[0])==request.POST["script"]):
                not_mis = True



    if (p.order_type == "SL"):
        if not_mis is True:

            try:
                order_id = kite.place_order(price=round(Price,1), trigger_price=trigPrice,
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_SL,
                                            product=kite.PRODUCT_CNC)


                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': p.order_type})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})

        else:

            try:
                order_id = kite.place_order(price=round(Price,1), trigger_price=trigPrice,
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_SL,
                                            product=kite.PRODUCT_MIS)


                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})
    else:
        print("Working")

        lprice = v["data"]["depth"]["sell"][0]["price"] + v["data"]["depth"]["sell"][0]["price"] * (p.cushion_price/100)
        if not_mis is True:

            try:
                order_id = kite.place_order(price=round(lprice,1),
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_LIMIT,
                                            product=kite.PRODUCT_CNC)

                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})

        else:

            try:
                order_id = kite.place_order(price=round(lprice,1),
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_LIMIT,
                                            product=kite.PRODUCT_MIS)

                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})







    #https://api.kite.trade/instruments/NSE/INFY?api_key=l5x8ay13aegnq946&access_token=5978ylw21tvnnvs3jallyt9r98yw6zbj


@csrf_exempt
def set_apikey(request):


    global kite
    global apiKey



    if  request.method == "POST":


        apiKey = request.POST["key"]

        request.session['apikey'] = apiKey

        kite = KiteConnect(api_key=apiKey)
        r = requests.get(kite.login_url())


        return render(request,'trademsg/set_access.html',context={"url":kite.login_url(),'data':r.text})



    else:
        return render(request,'trademsg/set_apikey.html')

@csrf_exempt
def reset(request):
    for key in list(request.session.keys()):
        del request.session[key]

    APIINFO.objects.all().delete()
    return redirect(reverse('trademsg:setapikey'))



@csrf_exempt
def token(request):
    kite = KiteConnect(api_key=apiKey)


    if 'access_token' in request.session:


        accessToken = request.session['access_token']
        kite = KiteConnect(api_key=request.session['apikey'])



        kite.set_access_token(accessToken)
        return redirect(reverse('trademsg:index'))


    if  request.method == "POST":


        request.session['access_token'] = request.POST["access_token"]
        request.session.set_expiry(how_many_seconds_until_midnight())
        accessToken = request.POST["access_token"]
        kite = KiteConnect(api_key=request.session['apikey'])

        p = APIINFO(no=1,api_key=request.session['apikey'],api_token=request.POST["access_token"],dattime=datetime.now())
        p.save()

        kite.set_access_token(accessToken)

        return redirect(reverse('trademsg:index'))
        # return render(request,"trademsg/trademsg.html")


@api_view(['GET', 'POST'])
@csrf_exempt
def sell(request):

    p = APIINFO.objects.latest('id')

    apiKey = p.api_key
    accessToken = p.api_token
    kite = KiteConnect(api_key=apiKey)
    kite.set_access_token(accessToken)


    r = requests.get(''.join(
        ["https://api.kite.trade/instruments/NSE/", request.POST["script"], "?api_key=", apiKey, '&access_token=',
         accessToken]))

    v = json.loads(r.text)

    trigPrice = v["data"]["depth"]["buy"][0]["price"] - 0.20
    Price = trigPrice - (trigPrice * (p.cushion_price/100))
    script_exp = int(round(p.script_exposure/v["data"]["depth"]["buy"][0]["price"]))


    not_mis = False

    with open(''.join([dir_path, "/mis_blocked.csv"])) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if (str(row[0]) == request.POST["script"]):
                not_mis = True

    if(p.order_type=="SL"):

        if not_mis is True:

            try:
                order_id = kite.place_order(price=round(Price,1), trigger_price=trigPrice,
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_SL,
                                            product=kite.PRODUCT_CNC)

                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})

        else:

            try:
                order_id = kite.place_order(price=round(Price,1), trigger_price=trigPrice,
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_SL,
                                            product=kite.PRODUCT_MIS)

                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})
    else:
        lprice = v["data"]["depth"]["buy"][0]["price"] - v["data"]["depth"]["buy"][0]["price"] *  (p.cushion_price/100)

        if not_mis is True:

            try:
                order_id = kite.place_order(price=round(lprice,1),
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_LIMIT,
                                            product=kite.PRODUCT_CNC)

                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})

        else:

            try:
                order_id = kite.place_order(price=round(lprice,1),
                                            tradingsymbol=request.POST["script"], variety=kite.VARIETY_REGULAR,
                                            exchange=kite.EXCHANGE_NSE,
                                            transaction_type=kite.TRANSACTION_TYPE_SELL,
                                            quantity=script_exp,
                                            order_type=kite.ORDER_TYPE_LIMIT,
                                            product=kite.PRODUCT_MIS)

                logging.info("Order placed. ID is: {}".format(order_id))

                return JsonResponse({'orderId': order_id})
            except Exception as e:
                logging.info("Order placement failed: {}".format(e))
                return JsonResponse({'orderFailed': "Failed"})


