import os
import time
import stomp
import pymysql
import sys
import json
import datetime

def connect_and_subscribe(conn):
    conn.start()
    conn.connect('admin','admin',wait=True)
    conn.subscribe(destination='/topic/tradeMsgTopic',id=1,ack='auto')


class MyListener(stomp.ConnectionListener):

    def __init__(self,conn):
        self.conn = conn


    def on_error(self, headers, message):
        print("received an error %s"%message)

    def on_message(self, headers, message):
        #print('Received a message %s' % message)
        con = pymysql.connect("localhost", 'root', 'welcome', "tradefront", use_unicode=True, charset="utf8")
        cur = con.cursor(pymysql.cursors.DictCursor)





        with con:
            json_data = json.loads(message)
            data = json_data
            print(json_data['record1'])

            json_data = data['record1']

            query = "INSERT INTO trade_message (Date_time,script,close_price,trade_pos,entry_price,SL,I_target_price,I_target_exit,I_target_PL,II_target_price,II_target_exit,II_target_PL,trailing_exit,trailing_float,share_float) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (
                datetime.datetime.fromtimestamp(json_data['date'] / 1e3), json_data['symbol'], json_data['closePrice'], json_data['tradePosition'], json_data['entryPrice'], json_data['sl'], json_data['target1Price'], json_data['target1ExitPrice'], json_data['target1PL'], json_data['target2Price'],json_data["target2ExitPrice"],json_data["target2PL"],json_data["trailingExitPrice"],json_data["tailingPL"],json_data["shareFloat"]))

            json_data = data['record2']
            print(json_data)

            query = "INSERT INTO trade_message (Date_time,script,close_price,trade_pos,entry_price,SL,I_target_price,I_target_exit,I_target_PL,II_target_price,II_target_exit,II_target_PL,trailing_exit,trailing_float,share_float) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query, (
                datetime.datetime.fromtimestamp(json_data['date'] / 1e3), json_data['symbol'], json_data['closePrice'], json_data['tradePosition'],
                json_data['entryPrice'], json_data['sl'], json_data['target1Price'], json_data['target1ExitPrice'],
                json_data['target1PL'], json_data['target2Price'], json_data["target2ExitPrice"],
                json_data["target2PL"], json_data["trailingExitPrice"], json_data["tailingPL"],
                json_data["shareFloat"]))

        print("processed message")




    def on_disconnected(self):
        print("disconnected")
        connect_and_subscribe(self.conn)




conn = stomp.Connection([('mach10.entityvibes.com', 61613)],heartbeats=(20000,0))
conn.set_listener('', MyListener(conn))
connect_and_subscribe(conn)
while True:
    time.sleep(30)

conn.disconnect()
