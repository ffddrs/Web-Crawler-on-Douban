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
    response_top25=requests.get(baseurl,headers=header)
    time.sleep(random.randint(3,5))
    response_top25.encoding='utf-8'
    print(response_top25.text)

crawl_top25()