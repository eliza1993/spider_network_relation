使用前提：
   安装小号scrapy框架
数据库格式：
# Dump of table GrabSite
# ------------------------------------------------------------

CREATE TABLE `GrabSite` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `siteDomain` varchar(100) DEFAULT NULL,
  `siteName` varchar(100) DEFAULT NULL,
  `webPageCount` int(10) DEFAULT '0',
  `totalOutLinkCuont` int(10) DEFAULT '0',
  `siteStatus` varchar(10) NOT NULL DEFAULT 'WAIT' COMMENT 'WAIT/WORKING/FINISH',
  `siteType` varchar(11) DEFAULT NULL COMMENT 'seed/outlink',
  `createTime` datetime DEFAULT NULL,
  `startGrabTime` datetime DEFAULT NULL,
  `endGrabTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `siteDomain` (`siteDomain`),
  KEY `createTime` (`createTime`),
  KEY `startGrabTime` (`startGrabTime`),
  KEY `endGrabTime` (`endGrabTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='siteStatus：WAIT/WORKING/FINISH\nsiteType：seed/outlink';



# Dump of table SiteGrabHistory
# ------------------------------------------------------------

CREATE TABLE `SiteGrabHistory` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `siteDomain` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `levels` int(2) DEFAULT NULL,
  `grabStatus` varchar(10) DEFAULT 'NEW' COMMENT 'NEW/WORKING/FINISH',
  `innerPageCount` int(10) DEFAULT '0',
  `outPageCount` int(10) DEFAULT '0',
  `createTime` datetime DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  `crawlCount` int(2) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
  KEY `siteDomain` (`siteDomain`),
  KEY `createTime` (`createTime`),
  KEY `lastUpdateTime` (`lastUpdateTime`),
  KEY `sitePage_status` (`siteDomain`,`grabStatus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table SiteRelation
# ------------------------------------------------------------

CREATE TABLE `SiteRelation` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `masterSite` varchar(100) DEFAULT NULL,
  `outLinkSite` varchar(100) DEFAULT NULL,
  `outLinkCount` int(10) DEFAULT '0',
  `createTime` datetime DEFAULT NULL,
  `lastUpdateTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `masterSite_2` (`masterSite`,`outLinkSite`),
  KEY `createTime` (`createTime`),
  KEY `lastUpdateTime` (`lastUpdateTime`),
  KEY `masterSite` (`masterSite`),
  KEY `outLinkSite` (`outLinkSite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
