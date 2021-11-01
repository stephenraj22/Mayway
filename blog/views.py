import pymongo
from django.shortcuts import render
from bson import json_util
from django.http import HttpResponse
from django.core.cache import cache
from pymongo import MongoClient
import json
import certifi
ca = certifi.where()
datum = {
        'trending_stocks': 'trending-stocks',
        'top_stock_losers': 'top-stock-losers',
        'top_stock_gainers': 'top-stock-gainers',
        '52_week_high': '52-week-high',
        '52_week_low': '52-week-low',
        'most_active_stocks': 'most-active-stocks'
}
f = open('blog/holy_bible.json')
bible_dict = json.load(f)
CONNECTION_STRING = "mongodb+srv://admincoinuser:r0mnnPMDNPou93Ya@cluster0.6ne7k.mongodb.net/test"
client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)


def index(request):
    if request.method == "GET":
        return render(request, 'blog/holy_bible.html')
    else:
        book = request.POST.get('book')
        chapter = request.POST.get('chapter')
        verse_from = request.POST.get('from')
        verse_to = request.POST.get('to')
        language = int(request.POST.get('language'))
        if chapter == '':
            chapter = '1'
        data = bible_dict[book][language][chapter]
        if verse_to == '':
            verse_to = len(data)
            verse_to_dup = verse_to
        else:
            verse_to = int(verse_to)
            verse_to_dup = verse_to
        if verse_from == '':
            verse_from = 1
        else:
            verse_from = int(verse_from)
        data = " ".join(data[verse_from-1:verse_to])
        res = {'data': data, 'book': bible_dict[book][0],
               'chapter': chapter, 'verse_from': verse_from, 'verse_to': verse_to_dup}
        return render(request, 'blog/holy_bible.html', res)


def crypto_index(request):
    last_update_crypto = cache.get('crypto')
    if last_update_crypto is None:
        dbname = client['crypto']
        collection_name = dbname['crypto_data']
        res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
        res = list(res)
        cache.set('crypto', res, 900)
        return HttpResponse(json.dumps(res[0]), content_type="application/json")
    else:
        return HttpResponse(json.dumps(last_update_crypto[0]), content_type="application/json")


def get_all_crypto_name(request):
    last_update_crypto = cache.get('crypto')
    if last_update_crypto is None:
        dbname = client['crypto']
        collection_name = dbname['crypto_data']
        res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
        res = list(res)
        cache.set('crypto', res, 900)
        return HttpResponse(json.dumps(list(res[0]['data'].keys())), content_type="application/json")
    else:
        return HttpResponse(json.dumps(list(last_update_crypto[0]['data'].keys())), content_type="application/json")


def crypto_get_single(request):
    last_update_crypto = cache.get('crypto')
    coin_name = request.GET.get('coin_name')
    if last_update_crypto is None:
        dbname = client['crypto']
        collection_name = dbname['crypto_data']
        res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
        res = list(res)
        cache.set('crypto', res, 900)
        if coin_name is None or coin_name not in res[0]['data'].keys():
            return HttpResponse(json.dumps("invalid coin name"), content_type="application/json")
        return HttpResponse(json.dumps(res[0]['data'][coin_name]), content_type="application/json")
    else:
        if coin_name is None or coin_name not in last_update_crypto[0]['data'].keys():
            return HttpResponse(json.dumps("invalid coin name"), content_type="application/json")
        return HttpResponse(json.dumps(last_update_crypto[0]['data'][coin_name]), content_type="application/json")


def currency(request):
    last_update_currency = cache.get('currency')
    if last_update_currency is None:
        dbname = client['currency_exchange']
        collection_name = dbname['currency_data']
        res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
        res = list(res)
        cache.set('currency', res, 900)
        return HttpResponse(json.dumps(res[0]), content_type="application/json")
    else:
        return HttpResponse(json.dumps(last_update_currency[0]), content_type="application/json")


def get_all_currency_name(request):
    last_update_currency = cache.get('currency')
    if last_update_currency is None:
        dbname = client['currency_exchange']
        collection_name = dbname['currency_data']
        res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
        res = list(res)
        cache.set('currency', res, 900)
        return HttpResponse(json.dumps(list(res[0]['data'].keys())), content_type="application/json")
    else:
        return HttpResponse(json.dumps(list(last_update_currency[0]['data'].keys())), content_type="application/json")


def currency_get_single(request):
    last_update_currency = cache.get('currency')
    currency_exchange = request.GET.get('exchange')
    if last_update_currency is None:
        dbname = client['currency_exchange']
        collection_name = dbname['currency_data']
        res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
        res = list(res)
        cache.set('currency', res, 900)
        if currency_exchange is None or currency_exchange not in res[0]['data'].keys():
            return HttpResponse(json.dumps("invalid exchange name"), content_type="application/json")
        return HttpResponse(json.dumps(res[0]['data'][currency_exchange]), content_type="application/json")
    else:
        if currency_exchange is None or currency_exchange not in last_update_currency[0]['data'].keys():
            return HttpResponse(json.dumps("invalid exchange name"), content_type="application/json")
        return HttpResponse(json.dumps(last_update_currency[0]['data'][currency_exchange]), content_type="application/json")


def stocks(request):
    category = request.GET.get('category')
    if category in datum.keys():
        last_update_stock = cache.get(category)
        if last_update_stock is None:
            dbname = client['indian_share_market']
            collection_name = dbname[datum[category]]
            res = collection_name.find({}, {"_id": 0, "ts": 0}).sort('ts', pymongo.DESCENDING).limit(1)
            res = list(res)
            cache.set(category, res, 900)
            return HttpResponse(json.dumps(res[0]), content_type="application/json")
        else:
            return HttpResponse(json.dumps(last_update_stock[0]), content_type="application/json")
    else:
        return HttpResponse(json.dumps("Invalid category"), content_type="application/json")

