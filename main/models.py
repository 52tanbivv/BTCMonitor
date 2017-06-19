from django.db import models

# Create your models here.



class BTCE(models.Model):
    """
    btc-e网页上的数据
    """
    ltc_to_btc = models.FloatField()
    eth_to_btc = models.FloatField()
    eth_to_ltc = models.FloatField()

    ctime = models.DateTimeField(auto_now_add=True)

class HuoBi(models.Model):
    """
    火币网上的数据
    """
    btc = models.FloatField()
    ltc = models.FloatField()
    eth = models.FloatField()

    ctime = models.DateTimeField(auto_now_add=True)

class PriceDifference(models.Model):
    """
    记录差价表
    """
    btc_e_price = models.FloatField("BTC-E价格")
    huobi_price = models.FloatField("火币价格")
    price_difference = models.FloatField("差价")

    data_type_choices = (
        (1, "LTC/BTC"),
        (2, "ETH/BTC"),
        (3, "ETH/LTC"),
    )
    data_type = models.IntegerField(choices=data_type_choices, verbose_name="数据类型")


    ctime = models.DateTimeField(auto_now_add=True)
