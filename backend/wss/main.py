#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from hbsdk import ApiClient, ApiError

ACCESS_KEY="c8b81ab5-1c479c95-1113c8c6-d1045"
SECRET_KEY="bc78194c-63dad026-d784cbf7-319df"

def main():
    client = ApiClient(ACCESS_KEY, SECRET_KEY)
    # get symbol:
    symbols = client.get('/v1/common/symbols')
    print(symbols)
    # get user info:
    userinfo = client.get('/v1/users/user')
    print(userinfo)
    # get all accounts:
    accs = client.get('/v1/account/accounts')
    print(accs)
    account_id = accs[0].id
    for acc in accs:
        subaccs = client.get('/v1/account/accounts/%s/balance' % acc.id)
        print(subaccs)
    time.sleep(2.0)
    # create order:
    order_id = client.post('/v1/order/orders', {
        'account-id': account_id,
        'amount': '0.02',
        'price': '1020.21',
        'symbol': 'ethcny',
        'type': 'buy-limit',
        'source': 'api'
    })
    print(order_id)
    # place order:
    client.post('/v1/order/orders/%s/place' % order_id)
    # get order details:
    order_info = client.get('/v1/order/orders/%s' % order_id)
    print(order_info)
    # cancel order:
    client.post('/v1/order/orders/%s/submitcancel' % order_id)
    # query order details:
    time.sleep(5.0)
    order_info = client.get('/v1/order/orders/%s' % order_id)
    print(order_info)

if __name__ == '__main__':
    main()
