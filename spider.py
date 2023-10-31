import json
import boto3
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings

class MySpiderAmys(scrapy.Spider):
    name = 'amys'
    
    def __init__(self, baseUrl=None, **kwargs):
        super(MySpiderAmys, self).__init__()
        self.baseUrl = baseUrl
        self.settings = get_project_settings()
        self.CLIENT = boto3.client('s3')
        self.BUCKET = self.settings.get('S3_BUCKET_NAME')
        self.FILE = self.settings.get('S3_FILE_NAME')
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MySpiderAmys, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        print('Opening {} spider'.format(spider.name))

    def spider_closed(self, spider):
        print('Closing {} spider'.format(spider.name))

    def start_requests(self):
        yield scrapy.Request(url=self.baseUrl, callback=self.parse)

    def parse(self, response):
        recipe = {}
        keysfields = self.settings.getlist('KEYS_FIELDS')
        valueSelectors = self.settings.getlist('VALUE_SELECTORS')

        for idx in range(len(keysfields)):
            if keysfields[idx] == 'recipeInstruction' or keysfields[idx] == 'recipeIngredient':
                recipe[keysfields[idx]] = response.xpath(valueSelectors[idx]).getall()
            else:
                recipe[keysfields[idx]] = response.xpath(valueSelectors[idx]).get("")

        try:
            recipeDataStream = bytes(json.dumps(recipe).encode("UTF-8"))
            self.CLIENT.put_object(Bucket=self.BUCKET, Key=self.FILE, Body=recipeDataStream)
        except Exception as e:
            self.logger.error(f"Unable to upload file to bucket: {self.BUCKET}. Error: {str(e)}")
