import datetime
from mysqlConnector import mysqlConnector

class SiteGrabHistory(object):
	"""docstring for SiteGrabHistory"""
	def __init__(self,mysqlConn):
		self.mysqlConn = mysqlConn

	def get_cursor(self):
		return self.mysqlConn.cursor()
	def insert_one(self,items = []):
		if self.has_url(items):
			return
			
		insert_sql = "insert into SiteGrabHistory(siteDomain,url,levels,grabStatus,innerPageCount,outPageCount,createTime,lastUpdateTime) "+"values(%s,%s,%s,%s,%s,%s,%s,%s)"

		insert_item  = []
		insert_item.append(items['siteDomain'])
		insert_item.append(items['url'])
		insert_item.append(items['levels'])
		insert_item.append(items['grabStatus'])
		insert_item.append(items['innerPageCount'])
		insert_item.append(items['outPageCount'])
		insert_item.append(items['createTime'])
		insert_item.append(items['lastUpdateTime'])
		cursor = self.get_cursor()
		cursor.execute(insert_sql,insert_item)
		self.mysqlConn.commit()


	def has_url(self,items = {}):
		query_sql = "select * from SiteGrabHistory where url = '%s' " % (items['url'])
		cursor = self.get_cursor()
		cursor.execute(query_sql)
		results = cursor.fetchall()
		if len(results) > 0:
			return True

		return False
		


	def query_by_domain_and_status(self,items = []):
		query_sql = "select id,siteDomain,url,levels,grabStatus,innerPageCount,outPageCount,createTime,lastUpdateTime ,crawlCount from SiteGrabHistory where siteDomain = '%s' and grabStatus = '%s' order by id asc limit 10" % (items['siteDomain'],items['grabStatus'])
		cursor = self.get_cursor()
		cursor.execute(query_sql)
		results = cursor.fetchall()

		items_res = []
		if len(results) > 0:
			for result in results:
				item = {}
				item['id'] = result[0]
				item['siteDomain'] = result[1]
				item['url'] = result[2]
				item['grabStatus'] = result[3]
				item['innerPageCount'] = result[4]
				item['outPageCount'] = result[5]
				item['createTime'] = result[6]
				item['lastUpdateTime'] = result[7]
				item['levels'] = result[8]
				item['crawlCount'] = result[9]
				items_res.append(item)
				print '==================---'
				print item
				print result


		return items_res


	# def query_by_domain_and_status(self,items = []):
	# 	query_sql = "select id,siteDomain,url,grabStatus,innerPageCount,outPageCount,createTime,lastUpdateTime from SiteGrabHistory where siteDomain = '%s' and grabStatus = '%s' order by id asc limit 100" % (items['siteDomain'],items['grabStatus'])
	# 	cursor = self.get_cursor()
	# 	cursor.execute(query_sql)
	# 	results = cursor.fetchall()

	# 	items_res = []
	# 	if len(results) > 0:
	# 		for result in results:
	# 			item = {}
	# 			item['id'] = result[0]
	# 			item['siteDomain'] = result[1]
	# 			item['url'] = result[2]
	# 			item['grabStatus'] = result[3]
	# 			item['innerPageCount'] = result[4]
	# 			item['outPageCount'] = result[5]
	# 			item['createTime'] = result[6]
	# 			item['lastUpdateTime'] = result[7]
	# 			items_res.append(item)

	# 	return items_res

	
	def query_by_url(self,url):
		query_sql = "select levels from SiteGrabHistory where url = '%s' " % (url)
		cursor = self.get_cursor()
		results = cursor.execute(query_sql)
		#results = cursor.fetchon()

		return results






	def update(self,items = []):

		update_sql = "update SiteGrabHistory set grabStatus = '%s' ,innerPageCount = %s,outPageCount=%s,lastUpdateTime='%s' where url = '%s' " %(items['grabStatus'],items['innerPageCount'],items['outPageCount'],items['lastUpdateTime'],items['url'])
		cursor = self.get_cursor()
		cursor.execute(update_sql)
		self.mysqlConn.commit()


	def update_crawl_count(self,items = []):

		update_sql = "update SiteGrabHistory set grabStatus = '%s' ,crawlCount = %s,lastUpdateTime='%s' where url = '%s' " %(items['grabStatus'],items['crawlCount'],items['lastUpdateTime'],items['url'])
		cursor = self.get_cursor()
		cursor.execute(update_sql)
		self.mysqlConn.commit()
		



def test_insert_one(siteGbHis):


	items = {}
	items['siteDomain'] = 'www.baidu.com'
	items['url'] = 'http://www.baidu.com'
	items['grabStatus'] = 'NEW'
	items['innerPageCount'] = 0
	items['outPageCount'] = 0
	items['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
	items['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

	siteGbHis.insert_one(items)
	

def test_query_by_domain_and_status(siteGbHis):
	items = {}
	items['siteDomain'] = 'www.baidu.com'
	items['grabStatus'] = 'NEW'

	print siteGbHis.query_by_domain_and_status(items)


def test_update(siteGbHis):
	items = {}
	items['siteDomain'] = 'www.baidu.com'
	items['url'] = 'http://www.baidu.com'
	items['grabStatus'] = 'FINSIH'
	items['innerPageCount'] = 1000
	items['outPageCount'] = 1000
	items['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

	siteGbHis.update(items)
	


if __name__ == '__main__':
	link = mysqlConnector()
	connect = link.openDb('127.0.0.1','root','','Freebuf_Secpulse')
	siteGbHis = SiteGrabHistory(connect)

	#test_insert_one(siteGbHis)
	test_query_by_domain_and_status(siteGbHis)
	test_update(siteGbHis)




