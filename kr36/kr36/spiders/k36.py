# -*- coding: utf-8 -*-
import scrapy
import json
import re
from kr36.items import Kr36Item


class K36Spider(scrapy.Spider):
    name = 'k36'
    allowed_domains = ['36kr.com']
    start_urls = ['https://36kr.com/information/web_news']

    def parse(self, response):
        first_id = response.xpath('//div[@class="kr-loading-more"]/div[@class="information-flow-list"]/div[1]/div[1]/@class').extract_first()
        first_id = str(first_id).split("-")[1]
        first_url = "https://36kr.com/pp/api/aggregation-entity?type=web_latest_article&b_id={}&per_page=100".format(first_id)
        yield scrapy.Request(
            url=first_url,
            callback=self.data_info
        )

    def data_info(self, response):
        item = Kr36Item()
        data = json.loads(response.text)
        items = data["data"]["items"]
        for ite in items:
            item["id"] = ite["post"]["id"]
            item["article_id"] = ite["id"]
            item["title"] = ite["post"]["title"]
            item["introduction"] = ite["post"]["summary"]
            item["time"] = ite["post"]["published_at"]
            item["introduction_img"] = ite["post"]["cover"]
            item["user_name"] = ite["post"]["user"]["name"]
            item["user_img"] = ite["post"]["user"]["avatar_url"]
            item["article_class"] = ite["post"]["feeds"][0]["name"]
            detail_url = "https://36kr.com/p/" + str(item["id"])
            yield scrapy.Request(
                            url=detail_url,
                            meta={"item": item},
                            callback=self.content_info
                        )
        next_url = "https://36kr.com/pp/api/aggregation-entity?type=web_latest_article&b_id={}&per_page=100".format(str(item["article_id"]))
        yield scrapy.Request(
            url=next_url,
            callback=self.data_info
        )

    def content_info(self, response):
        item = response.meta["item"]
        data = response.xpath('//div[@class="common-width content articleDetailContent kr-rich-text-wrapper"]//text()').extract()
        item["content"] = str(re.sub('.*\xa0.*?', "", str(data))).replace('\\xa0', '')
        yield item
