import json
import datetime
import os
import mimetypes
import zipfile
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.utils import timezone
from django.conf import settings

from main import models
from backend.electronicurrency import BTCECurrency, HuoBiECurrency

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO()

    def appendFile(self, file_path, file_name=None):
        u"从本地磁盘读取文件，并将其添加到压缩文件中"

        if file_name is None:
            p, fn = os.path.split(file_path)
        else:
            fn = file_name

        c = open(file_path, "rb").read()
        self.append(fn, c)

        return self

    def append(self, filename_in_zip, file_contents):
        """Appends a file with name filename_in_zip and contents of
                  file_contents to the in-memory zip."""

        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        """Returns a string with the contents of the in-memory zip."""

        self.in_memory_zip.seek(0)

        return self.in_memory_zip.read()

    def writetofile(self, filename):
        """Writes the in-memory zip to a file."""

        f = open(filename, "wb")
        f.write(self.read())
        f.close()


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
    data_file_path = "root\BTCMonitor\static\data_files\{}.csv".format(today)
    f = open(data_file_path, "w", encoding="utf-8")
    f.write("序号,"+"btc-e价格,"+"火币网价格,"+"差价,"+"类型,"+"时间\n")
    for i,row in enumerate(today_data,1):
        btc_e_price = row.btc_e_price
        huobi_price = row.huobi_price
        price_difference = row.price_difference
        ctime = row.ctime.strftime("%Y-%m-%d %H:%M")
        data_type = data_type_choices[int(row.data_type)-1][1]
        f.write("{},{},{},{},{},{}\n".format(i,btc_e_price,huobi_price,price_difference,data_type,ctime))
    models.DataFiles.objects.create(file_path=data_file_path)
    return HttpResponse("...")




def save_data(request):
    imz = InMemoryZip()
    file_objs = models.DataFiles.objects.filter(is_download=False)
    print(file_objs)
    for file in file_objs:
        imz.appendFile(file.file_path)

    data = imz.read()

    response = HttpResponse(mimetype="application/octet-stream")
    response["Content-Disposition"] = "attachment; log.zip"
    response["Content-Length"] = len(data)
    response.write(data)

    for file_obj in file_objs:
        file_obj.objects.update(is_download=True)

    return response











