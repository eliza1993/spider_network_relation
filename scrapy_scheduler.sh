#!/bin/bash/                                                                                                                                  

#cron 表达式 每5分钟执行 一次
#*/5 * * * *  sh /Users/huyi/networkR/networkR/scrapy_scheduler.sh
export PATH=$PATH:/usr/local/bin

cd /Users/Eliza/Spider/networkR

nohup scrapy crawl networkr >> /Users/Eliza/Spider/networkR/networkr.log 2>&1 &
