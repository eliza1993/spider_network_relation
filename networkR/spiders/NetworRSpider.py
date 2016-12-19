# -*- coding: utf-8 -*-
import scrapy
import datetime
from networkR.items import NetworkrItem
from networkR.dao.GrabSite import GrabSite
from networkR.dao.mysqlConnector import mysqlConnector
from networkR.dao.SiteGrabHistory import SiteGrabHistory

from scrapy.selector import Selector 

from networkR.util.UrlUtil import *

"""
获取站点关联数据：
1、从种子站点开始，获取站点首页源码
2、抽取首页源码中的链接，存储入库，记录该站点状态为working，直至该站点中的子页面全部处理完毕（FINISH)
3、访问库中存储的子页面链接，获取链接所指的页面源码，从源码中提取链接；
4、分析链接为指向站点内部还是其他站点，做count统计，还是直至1-3级目录的页面全部处理完毕。
5、选取下一个站点，重复步骤2-3
6、循环步骤1-5，直至站点列表中的所以站点都处理完毕

Args:
    url:需要提取的种子站点url，从domains.txt中提取

Return:
    站点链接信息，存储在表GrabSite（站点信息表），SiteGrabHistory（站点子页面信息表），SiteRelation（站点关联表）。

Created on 20161005
@author: Hu Yi
"""

class NetworRSpider(scrapy.Spider):

    '''
    读取种子站点
    '''
    name = "networkr"
    #allowed_domains = None #["http://www.i7gou.com"]
    start_urls = []
    file = open("domains.txt")
    for line in file:
        if line and len(line) > 0:
            line=line.strip('\n')
            line=line.strip('\r')
            seed_url = 'http://' + line
            start_urls.append(seed_url)
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
    print "Finish updated start_urls : ", start_urls
    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

    gbSite = None
    gbSiteHis = None


    def __init__(self):
        self.init_gb_site()
        self.init_site_grab_history()


    '''
    初始化url请求
    ''' 
    def start_requests(self):
        if self.start_urls and len(self.start_urls) > 0:
            self.handle_start_url()

        urls = self.plan_next_excute_urls()
        for url in urls:
            yield self.make_requests_from_url(url)
         

    '''
    处理返回的消息
    '''
    def parse(self, response):
        print response
        if response is None:
            return

        '''
        如果返回异常，进行异常处理
        '''
        if response.status != 200:
            #print "**********" 
            #print response.status
            #print "**********"
            self.handle_error_url(response.url)
            return

        url = handle_url(response.url)

        item = self.parse_item(url,response)

        return item


    def parse_item(self,url,response):
        item = NetworkrItem()
        item['siteDomain'] = get_domain(url)
        item['url'] = handle_url(url)

        innerPageArray,outPageArray = self.parse_page_links(item['siteDomain'],response)
        item['innerPageArray'] = innerPageArray
        item['outPageArray'] = outPageArray
        if item['siteDomain'] == item['url']:
            item['levels'] = 0
        else:
            levels = self.gbSiteHis.query_by_url(response.url)
            levels = levels + 1
            item['levels'] = levels

        return item



    def parse_page_links(self,domain,response):
        innerPageArray,outPageArray = [],[]

        totalLinks = []
        print response
        hxs=Selector(text=response.body)
        for aItem in hxs.xpath('//a'):
            link = aItem.xpath('@href').extract()
            if len(link) > 0:
                url = self.link_filter(domain,link[0])
                if not(url is None):
                    totalLinks.append(url)        
            
        
        for link in totalLinks:
            if domain in link:
                innerPageArray.append(handle_url(link))
            else:
                outPageArray.append(handle_url(link))

        return (innerPageArray,outPageArray)



    def link_filter(self,domain,link):
        if link is None:
            return link

        if 'javascript' in link:
            return None

        if 'http' in link:
            return link

        if 'www' in link:
            return link

        if '.com' in link:
            return link

        if '.cn' in link:
            return link

        if '.net' in link:
            return link

        if '#' in link:
            return None

        if link.endswith('/'):
            return None

        if not(domain in link):
            link = domain + '/' + link


        return link;

    '''
    存储要抓取的站点信息至GrabSite
    '''
    def handle_start_url(self):
        items = {}
        items['siteDomain'] = ''
        for url in self.start_urls:
            items['siteDomain'] = get_domain(url);
            result = self.gbSite.query_grab_site_by_domain(items)
            if result is None:
                items['siteDomain'] = get_domain(url)
                items['siteName'] = url
                items['webPageCount'] = 0
                items['totalOutLinkCuont'] = 0
                items['siteStatus'] = 'NEW' 
                items['siteType'] = 'seed'
                items['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                items['startGrabTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                items['endGrabTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                self.gbSite.insert_one(items)
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print "Finish handle start_urls"
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"



    def handle_error_url(self,url):
        items = {}
        items["grabStatus"] = 'FINISH'
        items["url"] = url
        items["siteDomain"] = get_domain(url)
        items['innerPageCount'] = 0
        items['outPageCount'] = 0
        items['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        self.gbSiteHis.update(items);
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
        print "Finish handle error_urls"
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"



    def init_gb_site(self):
        mysqlConn = mysqlConnector()
        dbConn = mysqlConn.openDb('127.0.0.1','root','mysql','Freebuf_Secpulse')
        self.gbSite = GrabSite(dbConn)

    def init_site_grab_history(self):
        mysqlConn = mysqlConnector()
        dbConn = mysqlConn.openDb('127.0.0.1','root','mysql','Freebuf_Secpulse')
        self.gbSiteHis = SiteGrabHistory(dbConn)


    def plan_next_excute_urls(self):
        items = {}
        items['siteStatus'] = 'WORKING'
        result = self.gbSite.query_grab_site_by_status(items)
        print "xxxxxxxx"
        print result
        if not(result is None):
            hItems = {}
            hItems['siteDomain'] = result['siteDomain']
            hItems['grabStatus'] = 'NEW'
            result =  self.gbSiteHis.query_by_domain_and_status(hItems)  
            print "11111===================="
            print result
            if not(result is None) and len(result) > 0:
                print result
                self.update_crawl_status(result)
                urls = []
                for res in result:
                    urls.append(res['url'])

                return urls

            hItems['siteStatus'] = 'FINISH'
            self.gbSite.update(hItems)

        
        items['siteStatus'] = 'NEW'
        result = self.gbSite.query_grab_site_by_status(items)
        if not(result is None):
            urls = []
            urls.append(result['siteDomain'])
            item = {}
            item['siteStatus'] = 'WORKING'
            item['siteDomain'] = result['siteDomain']
            self.gbSite.update(item)
            return urls;


        return []

    '''
    当目录等级大于3时，结束处理，设置为FINISH
    '''
    def update_crawl_status(self,results = []):
        newResult = [];
        for result in results:
            print result
            count = result['crawlCount']
            print "==========================="
            print count
            count = count + 1
            result['crawlCount'] = count
            if result['crawlCount'] >= 2:
                result['grabStatus'] = 'FINISH'  #grabStatus

            else:
                result['grabStatus'] = 'NEW'  #grabStatus

            result['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            self.gbSiteHis.update_crawl_count(result)






        






