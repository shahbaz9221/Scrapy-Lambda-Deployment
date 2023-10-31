"""
Scrapy Spider Module

This module defines a Scrapy spider for web scraping and data extraction. It uses AWS S3 for data storage and
custom settings defined in Scrapy's project settings.

The spider retrieves data from a specified URL and processes it according to pre-defined keys and value selectors.
Extracted data is then uploaded to an S3 bucket for storage.

For usage, configure Scrapy project settings with appropriate S3 bucket and file details, as well as the key-value
selectors to extract data.

Class:
------
MySpiderAmys: Defines a Scrapy spider for web scraping and data extraction.

Functions:
----------
__init__: Initialize the Scrapy spider and set up necessary settings.
from_crawler: Create a Scrapy spider instance from the crawler.
spider_opened: Perform actions when the spider is opened.
spider_closed: Perform actions when the spider is closed.
start_requests: Start the spider by sending an initial request to the specified URL.
parse: Parse the response, extract data, and upload it to an S3 bucket.

"""

import json
import boto3
import scrapy
from scrapy import signals
from conf import settings

class MySpiderAmys(scrapy.Spider):
    name = 'amys'

    def __init__(self, baseUrl=None, **kwargs):
        """
        Initialize the Scrapy spider with necessary settings.

        :param baseUrl: The URL to start the web scraping process.
        :param kwargs: Additional keyword arguments (unused in this function).
        """
        super(MySpiderAmys, self).__init__()
        self.baseUrl = baseUrl
        self.settings = settings
        self.CLIENT = boto3.client('s3')
        self.BUCKET = self.settings.get('S3_BUCKET_NAME')
        self.FILE = self.settings.get('S3_FILE_NAME')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Create a Scrapy spider instance from the crawler.

        :param crawler: The Scrapy crawler instance.
        :param args: Positional arguments (unused in this function).
        :param kwargs: Keyword arguments (unused in this function).
        :return: An instance of the Scrapy spider.
        """
        spider = super(MySpiderAmys, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        """
        Perform actions when the spider is opened.

        :param spider: The Scrapy spider instance.
        """
        print('Opening {} spider'.format(spider.name))

    def spider_closed(self, spider):
        """
        Perform actions when the spider is closed.

        :param spider: The Scrapy spider instance.
        """
        print('Closing {} spider'.format(spider.name))

    def start_requests(self):
        """
        Start the spider by sending an initial request to the specified URL.
        """
        yield scrapy.Request(url=self.baseUrl, callback=self.parse)

    def parse(self, response):
        """
        Parse the response, extract data, and upload it to an S3 bucket.

        :param response: The Scrapy response object containing web page data.
        """
        recipe = {}
        keysfields = self.settings.getlist('KEYS_FIELDS')
        valueSelectors = self.settings.getlist('VALUE_SELECTORS')

        # Use a dictionary comprehension to create the recipe dictionary
        recipe = {
            keysfields[idx]: response.xpath(valueSelectors[idx]).getall()
            if keysfields[idx] in ('recipeInstruction', 'recipeIngredient')
            else response.xpath(valueSelectors[idx]).get("")
            for idx in range(len(keysfields))
        }

        # Create and upload the JSON data in a single step
        try:
            recipeDataStream = bytes(json.dumps(recipe).encode("UTF-8"))
            self.CLIENT.put_object(Bucket=self.BUCKET, Key=self.FILE, Body=recipeDataStream)
        except Exception as e:
            self.logger.error(f"Unable to upload file to bucket: {self.BUCKET}. Error: {str(e)}")

