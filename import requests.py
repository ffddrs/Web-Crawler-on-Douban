# -*- codinig: utf-8 -*-
import requests
import random
import time
import string
from bs4 import BeautifulSoup
import pymysql
import re

baseurl="https://movie.douban.com/top250"

def fromurl2soup(url):
    header = {  
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36",
        "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
    }
    response=requests.get(url,headers=header)
    response.encoding='utf-8'
    soup=BeautifulSoup(response.text,'html.parser')
    return soup

def crawl_top25():
    try:
        soup_top25=fromurl2soup(baseurl)
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
        for i in range(len(movies)):
            movies[i]=movies[i].find('div',{'class':'hd'})\
                              .find('a')\
                              .get('href')
        return movies
    except Exception as e:
        print(f"抓取失败: {e}")
        return []

def parse_movie_detail(movie):

    def find_pure_text_tag(find_key,save_name,tag,join=False):
        for i in range(len(tag)):
            if(tag[i]==find_key):
                start=i
                for j in range(i,len(tag)):
                    if(tag[j]=='\n'):
                        end=j
                        break
                if(end-start==2):
                    movieinfo[save_name]=tag[i+1].strip()
                elif(end-start>2):
                    movieinfo[save_name]=tag[i+1:j]
                break
        try:
            movieinfo[save_name]
            if join==True:
                movieinfo[save_name]=''.join(movieinfo[save_name]).strip()     
        except:
            movieinfo[save_name]=None
        
    movieinfo={}
    soup_movie=fromurl2soup(movie)
    pointer=soup_movie.find('div',{'class':'top250'})\
                      .find_parent('div',{'id':'content'})
    
    movieinfo['top25No']=soup_movie.find('div',{'class':'top250'})\
                                   .find('span').get_text(strip=True)
    
    movieinfo['title']=pointer.find('span',{'property':'v:itemreviewed'}).get_text(strip=True)

    movieinfo['year']=pointer.find('span',{'class':'year'}).get_text(strip=True)[1:-1]

    pointer=pointer.find('div',{'class':'article'})
    
    directorlist=pointer.find('span',string='导演')\
                                 .find_parent('span')\
                                 .find('span',{'class':'attrs'})\
                                 .find_all('a')
    for i in range(len(directorlist)):
        directorlist[i]=directorlist[i].get_text(strip=True)
    movieinfo['director']=directorlist
    
    scriptwriterlist=pointer.find('span',string='编剧')\
                                 .find_parent('span')\
                                 .find('span',{'class':'attrs'})\
                                 .find_all('a')
    for i in range(len(scriptwriterlist)):
        scriptwriterlist[i]=scriptwriterlist[i].get_text(strip=True)
    movieinfo['scriptwriter']=scriptwriterlist   
    
    lead_performerlist=[]
    lead_performer_spanlist=pointer.find('span',string='主演')\
                                  .find_parent('span')\
                                  .find('span',{'class':'attrs'})\
                                  .find_all('span')
    if lead_performer_spanlist==[]:
           lead_performer_a_list=pointer.find('span',string='主演')\
                                     .find_parent('span')\
                                     .find('span',{'class':'attrs'})\
                                     .find_all('a')
           lead_performerlist=[lead_performer_a.get_text(strip=True) for lead_performer_a in lead_performer_a_list]
    else:
        for lead_performer_span in lead_performer_spanlist:
            lead_performerlist.append(lead_performer_span.find('a').get_text(strip=True))
    movieinfo['lead_performer']=lead_performerlist

    genrelist=pointer.find_all('span',{'property':'v:genre'})
    for i in range(len(genrelist)):
        genrelist[i]=genrelist[i].get_text(strip=True)
    movieinfo['genre']=genrelist

    pointer=pointer.find('span',string='制片国家/地区:')\
                   .find_parent('div',{'id':'info'})
    info_text_list=list(pointer.strings)

    find_pure_text_tag('制片国家/地区:','produced_country_or_region',info_text_list)
    
    find_pure_text_tag('语言:','language',info_text_list)

    initial_release_date_span_list=pointer.find_all('span',{'property':'v:initialReleaseDate'})
    initial_release_date_list=[initial_release_date_span.get_text(strip=True) for initial_release_date_span in initial_release_date_span_list]
    movieinfo['initial_release_date']=initial_release_date_list

    find_pure_text_tag('片长:','runtime',info_text_list,join=True)

    find_pure_text_tag('又名:','also_known_as',info_text_list)

    find_pure_text_tag('IMDb:','IMDb',info_text_list)

    find_pure_text_tag('官方网站:','official_site',info_text_list,join=True)

    print(movieinfo)
    
movies=crawl_top25()
for movie in movies:
    parse_movie_detail(movie)




