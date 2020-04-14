#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib.request
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
from stem import Signal
from stem.control import Controller
import json
import time


def pagevisit_torify(url_):
    session = requests.session()
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    page = session.get(url_)
    soup = BeautifulSoup(page.text, features="lxml")
    # to check for ip change use below
    # r = session.get('https://canihazip.com/s')
    # print('crawling in progress', r.text, url_)
    print('crawling in progress', url_)
    # renew tor ip
    # with Controller.from_port(port = 9051) as controller:
    #     controller.authenticate(password="my password")
    #     controller.signal(Signal.NEWNYM)

    return soup


def get_elements(config, url):
    soup = pagevisit_torify(url)
    content = {}
    # print(soup.select('body > div > div > div.col.col-lg-3 > div:nth-child(3) > p:nth-child(3)').encode('ascii', 'ignore').decode('ascii'))
    print(soup.select('body > div > div > div.col.col-lg-3 > div:nth-child(3) > p:nth-child(3)'))
    
    for key in config:
        selector = config[key]
        contents = soup.select(selector)
        print(selector, contents)
        if contents is not None:
            for c in contents:
                content[key].append(get_text_from_soup(c))
            # if pos.get('content'):
            #     content[key].append(contents.get(pos.get('content')))
            # else:
            #     for c in contents:
            #         content[key].append(get_text_from_soup(c))

    return content


def get_text_from_soup(elem):
    text = ''

    if isinstance(elem, NavigableString):
        text = elem
    elif isinstance(elem, Tag):
        text = elem.text
    else:
        text = elem

    return text.strip()


def write_to_csv(row, headernames):
    filename = 'output.csv'
    with open(filename, mode='a', encoding='utf-8') as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=headernames)

        if output_file.tell() == 0:
            csv_writer.writeheader()

        csv_writer.writerow(row)


def read_from_csv(path):
    with open(path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    return rows


if __name__ == "__main__":
    input_rows = read_from_csv('./source.csv')

    try:
        output_rows = read_from_csv('./output.csv')
    except:
        output_rows = []

    start_idx = len(output_rows)
    end_idx = len(input_rows)

    with open('config.json', 'r') as f:
        config = json.load(f)

    for i in range(start_idx, end_idx):
        print(input_rows[i]['url'])
        input_rows[i].update(get_elements(config, input_rows[i]['url']))
        write_to_csv(input_rows[i], input_rows[i].keys())
        # sleep a bit. just because
        if i % 100 == 0:
            time.sleep(5)
