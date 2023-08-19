#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker, exc
from dbsetup import *
import datetime
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--link")

args = parser.parse_args()
url = args.link

wordReport=[]
messageReport=[]

engine = create_engine('sqlite:///scrape.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
dbsession = DBSession()

class Spider(scrapy.Spider):
    name = "reddit"
    def start_requests(self):
        yield scrapy.Request(url=url, callback=self.parse)


    # overall -> <div class="thing ... noncollapsed comment">
    # catch_id -> automatic
    # message -> <div class="md"><p>
    # author -> <a class="author may-blank ...">"
    # catchdate -> datetime.now
    # website -> htpps://www.reddit.com


    def parse(self, response):
        count = 0
        comments = BeautifulSoup(response.text,features="lxml")
        title = '###'.join(comments.find('title').contents)
        comments = comments.find_all(['p','h1','h2','h3','h4','title'])
        words = [w.word for w in dbsession.query(Buzzwords.word)] # get list of buzzwords
        for word in words:
            collection=[]
            for comment in comments:
                if word in f'{comment.get_text()}'.lower(): # if buzzword is found
                    collection.append(comment.get_text())
                    wordReport.append(word)
                    messageReport.append(comment.get_text())
                    count+=1
            if len(collection)>0:
                # add to database
                new_catch = Catches(message='###'.join(collection),author="paragraph & Header", word=word, catchdate=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"), website=url)
                dbsession.add(new_catch)
                dbsession.commit()
                self.log(f'\n\n{word} is repetead {len(collection)} times in \n{collection}\n\n')
        self.log('Finished scraping. Found {0} possible occurrences'.format(count))
         # add to database
        new_report = Report( website=title , word='###'.join(wordReport), message='###'.join(messageReport))
        dbsession.add(new_report)
        dbsession.commit()

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'         # access as browser
})

process.crawl(Spider)
process.start()