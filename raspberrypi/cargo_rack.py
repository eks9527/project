# /usr/bin/env/python
# encoding: utf-8

import urllib2
from bs4 import BeautifulSoup


url = 'http://10.1.1.187:5002/'

def how_many_products():
    fin_url = url + 'how_many_products'
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    soup = BeautifulSoup(res, 'html.parser')
    ans = soup.find('h2').text
    print(ans)
    return ans

def delete_item():
    fin_url = url + 'delete_item'
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('Coke: - 1!')
    return

def add_item():
    fin_url = url + 'add_item'
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('Coke: + 1!')
    return

def update_plus_cart():
    fin_url = url + 'user/cart/plus/Liu/1'
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('add cart\'sproduct success!')
    return

def update_delete_cart():
    fin_url = url + 'user/cart/delete/Liu/1'
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('delete cart\'s product success!')
    return


def item_name_take(item_name):
    fin_url = url + '{}/take'.format(item_name)
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('{} be taken 1'.format(item_name))
    return

def item_name_re(item_name):
    fin_url = url + '{}/re'.format(item_name)
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('{} reback 1'.format(item_name))
    return

def to_kafka(tea):
    fin_url = url + 'to_kafka/{}'.format(tea)
    request = urllib2.Request(fin_url)
    res = urllib2.urlopen(request)
    print('send message to kafka {}').format(tea)
    return
