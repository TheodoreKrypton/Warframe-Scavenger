# encoding: utf-8

import requests
import bs4
import re
import json


def get_wm_url(n):
    return "https://warframe.market/items/" + n.replace("&", "and").lower().replace(" ", "_")


def get_name(n):
    search_res = re.search("(.+) (.+?$)", n)
    weapon_name = search_res.group(1)
    part_name = search_res.group(2)
    if weapon_name == "Kavasa":
        return "Kavasa Prime Collar " + part_name
    if part_name == "Limb":
        search_res = re.search("(.+) (.+?$)", weapon_name)
        weapon_name = search_res.group(1)
        part_name = search_res.group(2) + " " + part_name
    return weapon_name + " Prime " + part_name


if __name__ == '__main__':
    url = "https://warframe.huijiwiki.com/wiki/%E6%9D%9C%E5%8D%A1%E5%BE%B7%E9%87%91%E5%B8%81"
    html = requests.get(url).text
    bs = bs4.BeautifulSoup(html, "lxml")
    table = bs.find('table')
    parts = table.find_all('tr')[1:]
    for part in parts:
        ducats = part.find_all('td')[2].attrs['data-sort-value']
        if ducats == "45":  # 银垃圾
            name = get_name(part.td.attrs['data-sort-value'])
            url = get_wm_url(name)
            html = requests.get(url).text
            bs = bs4.BeautifulSoup(html, "lxml")
            json_str = bs.find('script', attrs={'id': 'application-state'}).text
            json_obj = json.loads(json_str)
            orders = json_obj['payload']['orders']

            for order in orders:
                if order['order_type'] == "sell" and order['user']['status'] == "ingame" and order['user']['region'] == "en" \
                        and order['platinum'] <= 2:  # 2p 以下
                    print name
