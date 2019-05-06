import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="l5x8ay13aegnq946")
url = kite.login_url()
print(url)



# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

#data = kite.generate_session("2j3U1oqdaX4VOkxmbDY163hWxeHxEMsA", api_secret="os7dy0wq69p2cxgmwjdqg6m1w1pb2pbk")
kite.set_access_token("eag3m652tp72h4hasgy18m7v7u8zji9x")

# Place an order
try:
    order_id = kite.place_order(

        tradingsymbol="SILVERMIC18APRFUT",variety = kite.VARIETY_REGULAR,
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=10,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_NRML)


    logging.info("Order placed. ID is: {}".format(order_id))
except Exception as e:
    logging.info("Order placement failed: {}".format(e))


print(kite.orders())