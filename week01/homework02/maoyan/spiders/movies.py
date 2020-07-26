# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MaoyanItem
from scrapy.selector import Selector

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']



    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        headers = {'Cookie': '__mta=55530900.1595498244881.1595613153893.1595684310126.7; uuid_n_v=v1; uuid=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; _csrf=d2e2e8539904705cff1d576dffa39ccb370e3b66b82266d7951a059eb02e1a84; mojo-uuid=0f1c6e86365e634f56d43d091689d2f2; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595498245; _lxsdk_cuid=1737b1b2adec8-07f24758072927-31627402-384000-1737b1b2adec8; _lxsdk=E87A9830CCCA11EABF2811F0086C462E97F42615A0D646198CE511D359158F0A; mojo-session-id={"id":"97292ee6ca12ff4fe4a973f52b4d28b3","time":1595699962261}; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595700125; __mta=55530900.1595498244881.1595684310126.1595700124909.8; _lxsdk_s=17387211f0b-400-c51-5d1%7C%7C7'}
        yield scrapy.Request(url, callback=self.parse, headers=headers)
    # url 请求访问的网址
    # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
    # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数

    def parse(self, response):
        movies = Selector(response).xpath('//div[@class="movie-hover-info"]')[0:10]
        for movie in movies:
            item = MaoyanItem()
            item['movie_name'] = movie.xpath('./div[1]/span[1]/text()').extract_first()
            item['movie_type'] = movie.xpath('./div[2]/text()').extract()[1].strip()
            item['release_date'] = movie.xpath('./div[4]/text()').extract()[1].strip()
            yield item
