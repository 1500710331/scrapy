# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

'''
<tr class="odd">
					<td class="l square"><a target="_blank" href="position_detail.php?id=43639&amp;keywords=&amp;tid=0&amp;lid=0">SA-腾讯社交广告测试开发工程师（研发中心 北京）</a></td>
					<td>技术类</td>
					<td>1</td>
					<td>北京</td>
					<td>2018-08-24</td>
				</tr>
'''
class TencentSpider(scrapy.Spider):
	offset = 0
	name = 'tencent'
	baseUrl = "https://hr.tencent.com/position.php?&start="
	#allowed_domains = ['https://hr.tencent.com/position.php']
	start_urls = [baseUrl + str(offset)]

	def parse(self, response):
		node_list = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
		for node in node_list:      

			item = TencentItem()

			item['positionName'] = node.xpath('./td[1]/a/text()').extract()[0]

			if len(node.xpath("./td[2]/text()")):
				item['positionType'] = node.xpath('./td[2]/text()').extract()[0]
			else:
				item['positionType'] = ''
			item['peopleNum'] = node.xpath('./td[3]/text()').extract()[0]
			item['workLocation'] = node.xpath('./td[4]/text()').extract()[0]
			item['pubdate'] = node.xpath('./td[5]/text()').extract()[0]
			item['position_url'] = node.xpath('./td[1]/a/@href').extract()[0]
	
		yield item


		if len(response.xpath("//a[@class='noactive' and @id='next']")) == 0:
			url = response.xpath("//a[@id='next']/@href").extract()[0]
			yield scrapy.Request("https://hr.tencent.com/" + url, callback = self.parse)