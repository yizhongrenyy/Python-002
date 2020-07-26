# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#from itemadapter import ItemAdapter


class MaoyanPipeline:
    def process_item(self, item, spider):
        with open("../movies.csv", "a+", encoding='utf-8') as f:
            f.write(f"\"{item['movie_name']}\",\"{item['movie_type']}\",\"{item['release_date']}\"\n")
        return item
