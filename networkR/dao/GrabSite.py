import MySQLdb
import datetime

from mysqlConnector import mysqlConnector
class GrabSite(object):
	"""docstring for GrabSite"""

	def __init__(self,mysqlConn):
		self.mysqlConn = mysqlConn


	def get_cursor(self):
		return self.mysqlConn.cursor()

	def insert_one(self,items = {}):
		item_one = self.query_grab_site_by_domain(items)
		if not(item_one is None):
			return

		insert_sql = 'insert into ' + 'GrabSite(siteDomain,siteName,webPageCount,totalOutLinkCuont,siteStatus,siteType,createTime,startGrabTime,endGrabTime) '+ 'values(%s,%s,%s,%s,%s,%s,%s,%s,%s);'

		if items is None:
			print 'items is None'
			return

		if len(items) != 9:
			print 'items len error'
			return

		item_value = []

		item_value.append(items['siteDomain'])
		item_value.append(items['siteName'])
		item_value.append(items['webPageCount'])
		item_value.append(items['totalOutLinkCuont'])
		item_value.append(items['siteStatus'])
		item_value.append(items['siteType'])
		item_value.append(items['createTime'])
		item_value.append(items['startGrabTime'])
		item_value.append(items['endGrabTime'])

		cursor = self.get_cursor()
		cursor.execute(insert_sql,item_value)
		self.mysqlConn.commit()


	def query_grab_site_by_status(self,items = {}):
		query_sql =  "select id,siteDomain,siteName,webPageCount,totalOutLinkCuont,siteStatus ,siteType ,createTime,startGrabTime,endGrabTime from GrabSite where siteStatus = '%s'" % (items['siteStatus'])
		cursor = self.get_cursor()
		cursor.execute(query_sql)
		results = cursor.fetchall()
		print 'ttttttttttttttt'
		print results
		item = None
		if len(results) > 0:
			item = {}
			result =  results[0]
			item['id'] = result[0]
			item['siteDomain'] = result[1]
			item['siteName'] = result[2]
			item['webPageCount'] = result[3]
			item['totalOutLinkCuont'] = result[4]
			item['siteStatus'] = result[5]
			item['siteType'] = result[6]
			item['createTime'] = result[7]
			item['startGrabTime'] = result[8]
			item['endGrabTime'] = result[9]

		return item

	def query_grab_site_by_domain(self,items = {}):
		query_sql =  "select id,siteDomain,siteName,webPageCount,totalOutLinkCuont,siteStatus ,siteType ,createTime,startGrabTime,endGrabTime from GrabSite where siteDomain = '%s'" % (items['siteDomain'])
		cursor = self.get_cursor()
		cursor.execute(query_sql)
		results = cursor.fetchall()
		
		item = None
		if len(results) > 0:
			item = {}
			result =  results[0]
			item['id'] = result[0]
			item['siteDomain'] = result[1]
			item['siteName'] = result[2]
			item['webPageCount'] = result[3]
			item['totalOutLinkCuont'] = result[4]
			item['siteStatus'] = result[5]
			item['siteType'] = result[6]
			item['createTime'] = result[7]
			item['startGrabTime'] = result[8]
			item['endGrabTime'] = result[9]

		return item

	def update(self,items = []):
		update_sql = "update GrabSite set siteStatus = '%s' where siteDomain = '%s'" % (items['siteStatus'],items['siteDomain'])
		
		cursor = self.get_cursor()
		cursor.execute(update_sql)
		self.mysqlConn.commit()


	def update_count(self,items = {}):
		query_sql =  "select webPageCount,totalOutLinkCuont from GrabSite where siteDomain = '%s'" % (items['siteDomain'])
		cursor = self.get_cursor()
		cursor.execute(query_sql,)
		result = cursor.fetchone()

		if result is None:
			print ' no record'
			return

		webPageCount = result[0] + items['innerPageCount']
		totalOutLinkCuont = result[1] + items['outPageCount']
		update_sql = "update GrabSite set webPageCount = %s, totalOutLinkCuont = %s where siteDomain = %s" #% (items['siteStatus'],items['siteDomain'])
		

		item_value = []
		item_value.append(webPageCount)
		item_value.append(totalOutLinkCuont)
		item_value.append(items['siteDomain'])

		cursor = self.get_cursor()
		cursor.execute(update_sql,item_value)
		self.mysqlConn.commit()
		


def test_query():
	link = mysqlConnector()
	connect = link.openDb('127.0.0.1','root','mysql','Freebuf_Secpulse')
	test = GrabSite(connect)
	time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#time = datetime.datetime.now()

	items = {}
	items['siteDomain'] ='www.hello.com'
	items['siteName'] ='aa'
	items['webPageCount'] = 0
	items['totalOutLinkCuont'] = 0
	items['siteStatus'] ='NEW'
	items['siteType'] ='seed'
	items['createTime'] = time
	items['startGrabTime'] = time
	items['endGrabTime'] = time

	result = test.query_grab_site_by_status(items)
	print 'query_grab_site_by_status = '
	print result
	result = test.query_grab_site_by_domain(items)
	print 'query_grab_site_by_status = '
	print result



def test_update():
	link = mysqlConnector()
	connect = link.openDb('192.168.31.160','root','','Spider')
	test = GrabSite(connect)
	time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#time = datetime.datetime.now()

	items = {}
	items['siteDomain'] ='www.hello.com'
	items['siteName'] ='hello'
	items['webPageCount'] = 6
	items['totalOutLinkCuont'] = 8
	items['siteStatus'] ='FINI'
	items['siteType'] ='seed'
	items['createTime'] = time
	items['startGrabTime'] = time
	items['endGrabTime'] = time

	test.update(items)
	print 'update successed'
	test.update_count(items)
	print 'update count successed'





if __name__ == '__main__':
	test_update()
	test_query()






