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

    try:
        movieinfo['summary']=soup_movie.find('span',{'class':'all hidden'}).get_text(strip=True)
    except:
        movieinfo['summary']=soup_movie.find('span',{'property':'v:summary'}).get_text(strip=True)

    pointer=soup_movie.find('div',{'class':'rating_wrap clearbox'})

    movieinfo['rating']=pointer.find('strong',{'class':'ll rating_num'}).get_text(strip=True)

    movieinfo['nums_of_rating_people']=pointer.find('a',{'class':'rating_people'})\
                                              .find('span',{'property':'v:votes'}).get_text(strip=True)
    
    ratings_on_weight={}
    for i in range(1,6):
        ratings_on_weight['{} star'.format(i)]=pointer.find('span',{'class':'stars{} starstop'.format(i)})\
                                                      .find_next_sibling('span',{'class':'rating_per'}).get_text(strip=True)
    movieinfo['ratings_on_weight']=ratings_on_weight

    rating_text_list=list(pointer.find_parent('div',{'id':'interest_sectl'})\
                            .find('div',{'class':'rating_betterthan'}).strings)
    rating_text_list.remove('\n')
    for i in range(len(rating_text_list)):
        rating_text_list[i]=rating_text_list[i].strip()
    movieinfo['rating_betterthan']=[rating_text_list[i]+rating_text_list[i+1] for i in range(0,len(rating_text_list),2)]

    movieinfo['comments_site']=soup_movie.find('div',{'id':'comments-section'})\
                      .find('h2')\
                      .find('a')\
                      .get('href')
    
    return movieinfo

def parse_comments_site(comments_url):

    comments_divs=[]

    def parse_comments_site_page(comments_page_url):
        nonlocal comments_divs
        comment_page_soup=fromurl2soup(comments_page_url)
        pointer=comment_page_soup.find('div',{'class':'mod-bd','id':'comments'})
        comments_divs+=pointer.find_all('div',{'class':'comment-item'})
        return comments_page_url[:-9]+\
               pointer.find('div',{'id':'paginator'})\
                      .find('a',string='后页 >')\
                      .get('href')
    
    pageurl=comments_url
    for i in range(3):
        pageurl=parse_comments_site_page(pageurl)

    return comments_divs

def star(str):
    star_pattern=re.compile(r'allstar(\d+)')
    return int(re.match(star_pattern,str[0])[1])/10

def parse_comments_div(comments_div):
    comment={}
    pointer=comments_div.find('div',{'class':'comment'})
    comment['movie_id']=count
    comment['user']=pointer.find('span',{'class':'comment-info'})\
                           .find('a')\
                           .get_text(strip=True)
    try:
        comment['star']=star(pointer.find('span',{'class':'comment-info'})\
                                    .find('span', class_=lambda x: x and 'allstar' in x)\
                                    .get('class'))
    except:
        comment['star']=None
    comment['time']=pointer.find('span',{'class':'comment-time'}).get_text(strip=True)
    comment['useful']=pointer.find('span',{'class':'votes vote-count'}).get_text(strip=True)
    comment['content']=pointer.find('p',{'class':'comment-content'})\
                              .find('span',{'class':'short'}).get_text(strip=True)
    return comment

def create_database():
    with pymysql.connect(host='localhost',user='root',password='password') as db:
        with db.cursor() as cursor:
            sql="CREATE DATABASE IF NOT EXISTS movies"
            try:
                cursor.execute(sql)
                print('数据库创建成功')
            except pymysql.MySQLError as e:
                print(f"创建数据库时发生错误：{e}")
  
def create_movies_table():
    with pymysql.connect(host='localhost',user='root',password='password',database='movies') as db:
        with db.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS comments_list")
            cursor.execute("DROP TABLE IF EXISTS movies_list")
            sql="""CREATE TABLE movies_list(
                id INT AUTO_INCREMENT PRIMARY KEY,
                top25No VARCHAR(20) NOT NULL,
                title VARCHAR(100) NOT NULL,
                year VARCHAR(20) NOT NULL,
                director VARCHAR(1000) NOT NULL,
                scriptwriter VARCHAR(1000) NOT NULL,
                lead_performer VARCHAR(1000) NOT NULL,
                genre VARCHAR(100) NOT NULL,
                produced_country_or_region VARCHAR(100) NOT NULL,
                language VARCHAR(50) NOT NULL,
                initial_release_date VARCHAR(200) NOT NULL,
                runtime VARCHAR(50) NOT NULL,
                also_known_as VARCHAR(200) NOT NULL,
                IMDb VARCHAR(30) NOT NULL,
                official_site VARCHAR(100),
                summary VARCHAR(2000) NOT NULL,
                rating VARCHAR(20) NOT NULL,
                nums_of_rating_people VARCHAR(20) NOT NULL,
                ratings_on_weight VARCHAR(100) NOT NULL,
                rating_betterthan VARCHAR(100) NOT NULL,
                comments_site VARCHAR(100) NOT NULL)
                """
            try:
                cursor.execute(sql)
                print('电影数据表创建成功')
            except pymysql.MySQLError as e:
                print(f"创建电影数据表时发生错误：{e}")
    
def create_comments_table():
    with pymysql.connect(host='localhost',user='root',password='password',database='movies') as db:
        with db.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS comments_list")
            sql="""CREATE TABLE comments_list(
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                user VARCHAR(50) NOT NULL,
                star VARCHAR(20),
                time VARCHAR(50) NOT NULL,
                useful VARCHAR(40) NOT NULL,
                content VARCHAR(2000) NOT NULL,
                CONSTRAINT fk_parent FOREIGN KEY (movie_id) REFERENCES movies_list(id))
                """
            try:
                cursor.execute(sql)
                print('评论数据表创建成功')
            except pymysql.MySQLError as e:
                print(f"创建评论数据表时发生错误：{e}")
    
def insert_movie_table(movieinfo):
    values=list(movieinfo.values())
    for i in range(len(values)):
        values[i]=str(values[i])
    values=tuple(values)
    with pymysql.connect(host='localhost',user='root',password='password',database='movies') as db:
        with db.cursor() as cursor:
            sql="""INSERT INTO movies_list(top25No,title,year,director,scriptwriter,lead_performer,genre,produced_country_or_region,language,initial_release_date,runtime,also_known_as,IMDb,official_site,summary,rating,nums_of_rating_people,ratings_on_weight,rating_betterthan,comments_site)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
            try:
                cursor.execute(sql,values)
                db.commit()
                print('电影数据插入成功')
            except pymysql.MySQLError as e:
                db.rollback()
                print(f"电影数据插入时发生错误：{e}")


def insert_comments_table(comments_list):
    values=tuple(comments_list.values())
    with pymysql.connect(host='localhost',user='root',password='password',database='movies') as db:
        with db.cursor() as cursor:
            sql="""INSERT INTO comments_list(movie_id,user,star,time,useful,content)
                values(%s,%s,%s,%s,%s,%s)
                """
            try:
                cursor.execute(sql,values)
                db.commit()
                print('评论数据插入成功')
            except pymysql.MySQLError as e:
                db.rollback()
                print(f"评论数据插入时发生错误：{e}")

count=1    
create_database()
create_movies_table()
create_comments_table()
movies=crawl_top25()
for movie in movies:
    movieinfo=parse_movie_detail(movie)
    insert_movie_table(movieinfo)
    comments_dives=parse_comments_site(movieinfo['comments_site'])
    for comments_div in comments_dives:
        comment=parse_comments_div(comments_div)
        insert_comments_table(comment)
    count+=1
print("爬取完毕")





