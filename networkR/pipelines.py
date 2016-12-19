# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import datetime

from networkR.dao.SiteGrabHistory import SiteGrabHistory
from networkR.dao.SiteRelation import SiteRelation
from networkR.dao.GrabSite import GrabSite
from networkR.dao.mysqlConnector import mysqlConnector

class NetworkrPipeline(object):
	"""
		item:url\innerPageArr\outPageArr
	"""

	siteReDic = {}
	siteGbDic = {}
	siteRelation = None
	siteGrabHis = None
	siteGb = None


	def __init__(self):
		self.init_site_relation()
		self.init_site_grab_his()
		self.init_site_grab()


	def init_site_relation(self):
		mysqlConn = mysqlConnector()
		dbConn = mysqlConn.openDb('127.0.0.1','root','mysql','Freebuf_Secpulse')
		self.siteGrabHis = SiteGrabHistory(dbConn)

	def init_site_grab_his(self):
		mysqlConn = mysqlConnector()
		dbConn = mysqlConn.openDb('127.0.0.1','root','mysql','Freebuf_Secpulse')
		self.siteRelation = SiteRelation(dbConn)

	def init_site_grab(self):
		mysqlConn = mysqlConnector()
		dbConn = mysqlConn.openDb('127.0.0.1','root','mysql','Freebuf_Secpulse')
		self.siteGb = GrabSite(dbConn)

	def process_item(self, item, spider):
		"""
		验证 插入 更新
		"""

		if item is None:
			print '*******************'
			print 'None'
			return

		if len(item) == 0:
			print 'size is zero'
			return

		innerPageArray = item['innerPageArray']
		outPageArray = item['outPageArray']
		levels = item['levels']

		insertItems = {}
		if levels < 2:
			for index in range(0,len(innerPageArray)):
				insertItems["grabStatus"] = 'NEW'
				insertItems["url"] = innerPageArray[index]
				insertItems["siteDomain"] = self.get_domain(innerPageArray[index])
				insertItems['levels'] = levels
				insertItems['innerPageCount'] = 0
				insertItems['outPageCount'] = 0
				insertItems['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				insertItems['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self.siteGrabHis.insert_one(insertItems);	


			for index in range(0,len(outPageArray)):
				insertItems["grabStatus"] = 'NEW'
				insertItems["url"] = outPageArray[index]
				insertItems["siteDomain"] = self.get_domain(outPageArray[index])
				insertItems['levels'] = levels
				insertItems['innerPageCount'] = 0
				insertItems['outPageCount'] = 0
				insertItems['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				insertItems['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self.siteGrabHis.insert_one(insertItems);
				
				if not self.siteGbDic.has_key(insertItems["siteDomain"]):
					gbSiteItem = {}
					gbSiteItem['siteDomain'] = insertItems["siteDomain"]
					gbSiteItem['siteName'] = insertItems["siteDomain"]
					gbSiteItem['webPageCount'] = 0
					gbSiteItem['totalOutLinkCuont'] = 0
					gbSiteItem['siteStatus'] = 'NEW' 
					gbSiteItem['siteType'] = 'outlink'
					gbSiteItem['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
					gbSiteItem['startGrabTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
					gbSiteItem['endGrabTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
					self.siteGb.insert_one(gbSiteItem)

				#建立 site relation 关系
				self.handle_site_relation(item['siteDomain'],insertItems["siteDomain"])		
			



		insertItems["grabStatus"] = 'FINISH'
		insertItems["url"] = item['url']
		insertItems["siteDomain"] = item['siteDomain']
		insertItems['innerPageCount'] = len(innerPageArray)
		insertItems['outPageCount'] = len(outPageArray)
		insertItems['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
		self.siteGrabHis.update(insertItems);
		print insertItems
		self.siteGb.update_count(insertItems)


	def get_domain(self,url):
		http_pro = ''
		if 'http://' in url:
			http_pro = 'http://'
			url = url[7:]

		if 'https://' in url:
			http_pro = 'https://'
			url = url[8:]

		if '/' in url:
			index = url.index('/')
			url = url[0:index]

		url = http_pro + url
		return url

	"""
	def get_sitename(self,url):
		sitename = ''
		/head/title[1]
	"""
        


	def close_spider(self, spider):
		pass

	def handle_site_relation(self,masterSite,outLinkSite):
		if self.has_site_relation(masterSite,outLinkSite):
			self.increase(masterSite,outLinkSite)
			return

		items = {}
		items['masterSite'] = masterSite;
		items['outLinkSite'] = outLinkSite
		items['outLinkCount'] = 1
		items['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
		items['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

		self.siteRelation.insert_one(items)
		key = masterSite + "_" + outLinkSite
		self.siteReDic[key] = key


	def has_site_relation(self,masterSite,outLinkSite):
		key = masterSite + "_" + outLinkSite
		if self.siteReDic.has_key(key):
			return True

		items = {}
		items['masterSite'] = masterSite;
		items['outLinkSite'] = outLinkSite;
		return self.siteRelation.has_site_relation(items)

	def increase(self,masterSite,outLinkSite):
		items = {}
		items['masterSite'] = masterSite;
		items['outLinkSite'] = outLinkSite;

		self.siteRelation.increase_one(items)





if __name__ == '__main__':
	url = 'https://www.baidu.com'
	url2 = 'http://www.baidu.com'

	siteGrabHis = SiteGrabHistory(None)
	pipeline = NetworkrPipeline(siteGrabHis)
	print pipeline.get_domain(url)
	print pipeline.get_domain(url2)

	items = {}
	pipeline.process_item(items)
