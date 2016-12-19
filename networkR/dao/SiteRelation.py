from mysqlConnector import mysqlConnector
import datetime

class SiteRelation(object):
	"""docstring for SiteRelation"""
	def __init__(self,mysqlConn):
		self.mysqlConn = mysqlConn
		

	def get_cursor(self):
		return self.mysqlConn.cursor()

	def insert_one(self,items = []):
		insert_sql = "insert into SiteRelation(masterSite,outLinkSite,outLinkCount,createTime,lastUpdateTime) values(%s,%s,%s,%s,%s)"
		insert_item  = []
		insert_item.append(items['masterSite'])
		insert_item.append(items['outLinkSite'])
		insert_item.append(items['outLinkCount'])
		insert_item.append(items['createTime'])
		insert_item.append(items['lastUpdateTime'])
		cursor = self.get_cursor()
		cursor.execute(insert_sql,insert_item)
		self.mysqlConn.commit()


	def has_site_relation(self,items = {}):
		query_sql = "select * from SiteRelation where masterSite = '%s' and outLinkSite = '%s'" %(items['masterSite'],items['outLinkSite'])
		cursor = self.get_cursor()
		cursor.execute(query_sql)
		results = cursor.fetchall()
		return len(results) > 0

	def increase_one(self,items = {}):
		query_sql = "select outLinkCount from SiteRelation where masterSite = '%s' and outLinkSite = '%s'" %(items['masterSite'],items['outLinkSite'])
		cursor = self.get_cursor()
		cursor.execute(query_sql)
		results = cursor.fetchall()
		print results
		if len(results) > 0:
			result = results[0]
			count = result[0] + 1
			update_sql = "update SiteRelation set outLinkCount = %s where masterSite = '%s' and outLinkSite = '%s'" %(count,items['masterSite'],items['outLinkSite'])
			cursor.execute(update_sql)
			self.mysqlConn.commit()



def test_insert_one(siteRel):
	items = {}
	items['masterSite'] = 'www.baidu.com'
	items['outLinkSite'] = 'www.tongdun.com'
	items['outLinkCount'] = 100
	items['createTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
	items['lastUpdateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
	siteRel.insert_one(items)
	

def test_has_site_relation(siteRel):
	items = {}
	items['masterSite'] = 'www.baidu.com'
	items['outLinkSite'] = 'www.tongdun.com'
	print siteRel.has_site_relation(items)


def test_increase_one(siteRel):
	items = {}
	items['masterSite'] = 'www.baidu.com'
	items['outLinkSite'] = 'www.tongdun.com'
	siteRel.increase_one(items)
	
	

if __name__ == '__main__':
	link = mysqlConnector()
	connect = link.openDb('127.0.0.1','root','','Freebuf_Secpulse')
	siteRel = SiteRelation(connect)

	#test_insert_one(siteRel)
	test_has_site_relation(siteRel)
	test_increase_one(siteRel)
