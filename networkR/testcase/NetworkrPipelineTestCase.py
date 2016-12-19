#!/usr/bin/python
# -*- coding: utf-8 -*-

from networkR.networkR.pipelines import NetworkrPipeline


if __name__ == '__main__':
	url = 'https://www.baidu.com'
	url2 = 'http://www.baidu.com'
	pipeline = NetworkrPipeline()
	print pipeline.get_domain(url)
	print pipeline.get_domain(url2)