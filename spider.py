import json
import boto3
import scrapy
from scrapy import signals

class MySpiderAmys(scrapy.Spider):
    name = 'amys'
    
    CLIENT = boto3.client('s3')
    BUCKET = "scrape-url-data"
    FILE = 'RecipeData.json'
    
    def __init__(self, name=None, **kwargs):
        print(kwargs)
        self.baseUrl = kwargs.get("baseUrl")
        del kwargs['baseUrl']
        self.keysfields = list(kwargs.keys())
        self.valueSelectors = list(kwargs.values())
        

        
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
        print(self.keysfields)
        print(self.valueSelectors)
        for idx in range(len(self.keysfields)):
            if self.keysfields[idx] == 'recipeInstruction' or self.keysfields[idx] == 'recipeIngredient':
                recipe[self.keysfields[idx]] = response.xpath(f"{self.valueSelectors[idx]}").getall()
            else:
                recipe[self.keysfields[idx]] = response.xpath(f"{self.valueSelectors[idx]}").get("")
        print(recipe)
        try:
            recipeDataStream = bytes(json.dumps(recipe).encode("UTF-8"))
            self.CLIENT.put_object(Bucket=self.BUCKET, Key=self.FILE, Body=recipeDataStream)
        except:
            print("unable to upload file to bucket: {}" %self.BUCKET)
