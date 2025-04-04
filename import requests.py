# -*- codinig: utf-8 -*-
import requests
import random
import time
import string
from bs4 import BeautifulSoup
import pymysql
import re

baseurl="https://movie.douban.com/top250"

def crawl_top25():
    header = {  
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36",
        "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    }
    try:
        response_top25=requests.get(baseurl,headers=header)
        response_top25.encoding='utf-8'
        soup_top25=BeautifulSoup(response_top25.text,'html.parser')
        pointer=soup_top25.find('h1',string='豆瓣电影 Top 250')
        if not pointer:
            pointer=[]
        target_div=pointer.find_parent('div',{'id':'content'})\
                          .find('div',{'class':'article'})
        if not target_div:
            target_div=[]
        try:
            movies=target_div.ol.find_all('li')
        except:
            movies=[]
        for movie in movies:
            movie=movie.find('div',{'class':'hd'})\
                       .find('a')\
                       .get('href')
        return movies
    except Exception as e:
        print(f"抓取失败: {e}")
        return []

        

crawl_top25()


