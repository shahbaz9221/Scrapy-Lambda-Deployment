from scrapy.cmdline import execute

def handler(event=None, context=None):
    elements = event.get("elements", [])
    
    if elements:
        cmdLine = [
            "scrapy",
            "runspider",
            "spider.py",
        ]
        
        cmdLine.extend(f"-a {element.get('fieldName')}={element.get('xpath', element.get('baseUrl'))}" for element in elements)
        
        execute(cmdLine)
