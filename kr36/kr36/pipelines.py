# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import csv
import hashlib


class Kr36MongodbPipeline(object):
    def process_item(self, item, spider):
        sourse = str(item['id']) + item['title']
        hashvalue = hashlib.sha256(sourse.encode()).hexdigest()
        item["_id"] = hashvalue
        client = MongoClient(host='127.0.0.1', port=27017)
        cliention = client["k36"]["article_info"]
        cliention.insert(item)
        print("有一条新文章入库...")
        return item


class Kr36DataToCsvPipeline(object):
    def __init__(self):
        self.f = open("36kr.csv", "w", encoding='utf-8')
        self.writer = csv.writer(self.f)
        self.writer.writerow(['文章id', '标题', '简介', '发布时间', '简介图片', '作者', '作者头像', '分类', '正文'])

    def process_item(self, item, spider):
        hose_list = [item['id'], item['title'], item['introduction'], item['time'],item['introduction_img'], item['user_name'], item['user_img'], item['article_class'], item['content']]
        self.writer.writerow(hose_list)
        return item

    def close_spider(self, spider):  # 关闭
        # self.writer.close()
        self.f.close()
