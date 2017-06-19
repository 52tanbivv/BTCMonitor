#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM

import json

import requests
from bs4 import BeautifulSoup


class HuoBiECurrency:
    def __init__(self):
        self.btc_url = "https://api.btctrade.com/api/ticker?coin=btc"
        self.ltc_url = "https://api.btctrade.com/api/ticker?coin=ltc"
        self.eth_url = "https://api.btctrade.com/api/ticker?coin=eth"

    def get_html(self, url):
        headers = {}
        response = requests.get(url, headers=headers)
        return response.text

    @property
    def currency_last_num(self):
        btc = json.loads(self.get_html(self.btc_url))
        ltc = json.loads(self.get_html(self.ltc_url))
        eth = json.loads(self.get_html(self.eth_url))

        return {
            "btc": btc.get("last"),
            "ltc": ltc.get("last"),
            "eth": eth.get("last"),
        }


class BTCECurrency:
    def __init__(self):
        self.url = "https://btc-e.com/exchange/ltc_btc"

    @property
    def btc_e_num(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        ltc_btc_number = soup.find(id="last10").text
        eth_btc_number = soup.find(id="last40").text
        eth_ltc_number = soup.find(id="last42").text
        return {
            "ltc_to_btc": ltc_btc_number,
            "eth_to_btc": eth_btc_number,
            "eth_to_ltc": eth_ltc_number
        }

