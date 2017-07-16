# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
from scrapy.utils.project import get_project_settings

import os

class EromangaPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['manga']:
            yield Request(img)

    def file_path(self, request, response=None, info=None):
        imgname = request.url.split('/')[-1]
        return imgname

    def item_completed(self, results, item, info):
        for result in [x for ok, x in results if ok]:
            path = result['path']
            manga_title = item['title']
            storage = get_project_settings().get('IMAGES_STORE')

            target_path = os.path.join(storage, manga_title, os.path.basename(path))
            path = os.path.join(storage, path)

            if not os.path.exists(os.path.join(storage, manga_title)):
                os.makedirs(os.path.join(storage, manga_title))
            try:
                os.rename(path, target_path)
            except:
                pass

        if self.IMAGES_RESULT_FIELD in item.fields:
            item[self.IMAGES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item
