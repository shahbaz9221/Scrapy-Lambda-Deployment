"""
Scrapy Lambda Handler

This module defines a function for running a Scrapy spider with specified elements. The function, 
`run_scrapy_spider`, takes a dictionary `event` containing elements and optional context, and 
executes a Scrapy spider with the provided arguments.

Example Usage:
---------------
To run the Scrapy spider using this module, ensure that you have Scrapy and the necessary dependencies 
installed. Define an `event` dictionary with elements, where each element is a dictionary containing 
a "fieldName" and "xpath" or "baseUrl" key-value pair. Then, call the `run_scrapy_spider` function with 
the `event` dictionary.

Example event:
    example_event = {
        "elements": [
            {"fieldName": "field1", "xpath": "xpath1"},
            {"fieldName": "field2", "baseUrl": "base1"},
        ]
    }
    
    run_scrapy_spider(event=example_event)

Note:
-----
- Make sure you have Scrapy installed and configured with the desired spider before using this module.
- Customize the event dictionary according to your specific requirements and spider configuration.
- You can modify the `run_scrapy_spider` function for more advanced use cases if needed.

"""


from scrapy.cmdline import execute

def run_scrapy_spider(event=None, context=None):
    """
    Run a Scrapy spider with the given elements.

    :param event: A dictionary containing elements to pass as spider arguments.
    :param context: The Lambda execution context (unused in this function).
    """
    elements = event.get("elements", [])

    if elements:
        cmdLine = [
            "scrapy",
            "runspider",
            "spider.py",
        ]

        cmdLine.extend(f"-a {element.get('fieldName')}={element.get('xpath', element.get('baseUrl'))}" for element in elements)

        execute(cmdLine)

if __name__ == '__main__':
    # Define an example event for testing
    example_event = {
        "elements": [
            {"fieldName": "field1", "xpath": "xpath1"},
            {"fieldName": "field2", "baseUrl": "base1"},
        ]
    }
    
    run_scrapy_spider(event=example_event)
