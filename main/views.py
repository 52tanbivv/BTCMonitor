import json
import datetime
import os
import mimetypes

from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.utils import timezone
from django.conf import settings

from main import models
from backend.electronicurrency import BTCECurrency, HuoBiECurrency

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):

    return render(request, 'index.html')



def updata(request):
    """
    更新数据
    """

    print('start updata!')
    btce_currency = BTCECurrency()
    huobie_currency = HuoBiECurrency()
    btc_e = btce_currency.btc_e_num
    huobi_e = huobie_currency.currency_last_num

    models.BTCE.objects.create(
        ltc_to_btc=btc_e['ltc_to_btc'],
        eth_to_btc=btc_e['eth_to_btc'],
        eth_to_ltc=btc_e['eth_to_ltc']
    )

    models.HuoBi.objects.create(
        btc=huobi_e['btc'],
        ltc=huobi_e['ltc'],
        eth=huobi_e['eth']
    )

    ltc_to_btc_btc_e_price = 1/float(btc_e['ltc_to_btc'])
    eth_to_btc_btc_e_price = 1/float(btc_e['eth_to_btc'])
    eth_to_ltc_btc_e_price = 1/float(btc_e['eth_to_ltc'])
    ltc_to_btc_huobi_price = float(huobi_e['btc'])/float(huobi_e['ltc'])
    eth_to_btc_huobi_price = float(huobi_e['btc'])/float(huobi_e['eth'])
    eth_to_ltc_huobi_price = float(huobi_e['ltc'])/float(huobi_e['eth'])

    models.PriceDifference.objects.create(
        btc_e_price = ltc_to_btc_btc_e_price,
        huobi_price = ltc_to_btc_huobi_price,
        price_difference = ltc_to_btc_btc_e_price-ltc_to_btc_huobi_price,
        data_type = 1
    )
    models.PriceDifference.objects.create(
        btc_e_price=eth_to_btc_btc_e_price,
        huobi_price=eth_to_btc_huobi_price,
        price_difference=eth_to_btc_btc_e_price - eth_to_btc_huobi_price,
        data_type=2
    )
    models.PriceDifference.objects.create(
        btc_e_price=eth_to_ltc_btc_e_price,
        huobi_price=eth_to_ltc_huobi_price,
        price_difference=eth_to_ltc_btc_e_price - eth_to_ltc_huobi_price,
        data_type=3
    )


    context = {
        'btc_e':btc_e,
        'huobi_e':huobi_e
    }

    print(context)

    return HttpResponse(json.dumps(context))


def save(request):
    """
    将当天的数据保存为excel
    """
    now = timezone.now()
    start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)

    today_data = models.PriceDifference.objects.filter(ctime__gt=start)
    print(BASE_DIR)
    data_type_choices = models.PriceDifference.data_type_choices
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    f = open("static/data_files/{}.csv".format(today),"w")
    f.write("序号,"+"btc-e价格,"+"火币网价格,"+"差价,"+"类型,"+"时间\n")
    for i,row in enumerate(today_data,1):
        btc_e_price = row.btc_e_price
        huobi_price = row.huobi_price
        price_difference = row.price_difference
        ctime = row.ctime.strftime("%Y-%m-%d %H:%M")
        data_type = data_type_choices[int(row.data_type)-1][1]
        f.write("{},{},{},{},{},{}\n".format(i,btc_e_price,huobi_price,price_difference,data_type,ctime))
    the_file = "static/data_files/{}.csv".format(today)
    filename = os.path.join(BASE_DIR, the_file)
    print(filename)
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Encoding'] = 'utf-8'
    response['Content-Disposition'] = 'attachment;filename=%s' % filename
    return response











