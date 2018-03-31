# -*- coding: utf-8 -*-
#!/usr/bin/python3
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.conf import settings


class ScrapycommoditPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    host = 'localhost'
    user = 'root'
    password = ''
    dbname = 'test'
    db = None
    cursor = None
    sql = 'INSERT INTO item(itemId,itemTitle,itemPrice,itemImg) VALUES("%s","%s","%s","%s")'

    def __init__(self):
        self.host = settings['MYSQL_HOST']
        self.user = settings['MYSQL_USER']
        self.password = settings['MYSQL_PASSWORD']
        self.dbname = settings['MYSQL_DB_NAME']

    def open_spider(self, spider):
        try:
            self.db = pymysql.connect(
                self.host, self.user, self.password, self.dbname, use_unicode=True, charset="utf8")
            self.cursor = self.db.cursor()
        except Exception as e:
            spider.logger.error(e)

    def close_spider(self, spider):
        try:
            self.db.commit()
            self.db.close()
        except Exception as e:
            spider.logger.error(e)

    def process_item(self, item, spider):
        spider.logger.info(item)
        try:
            result = self.cursor.execute(self.sql % (float(item['itemId']), str(
                item['itemTitle']), str(item['itemPrice']), str(item['itemImg'])))
            spider.logger.info("result")
            spider.logger.info(result)
        except Exception as e:
            spider.logger.error(e)
