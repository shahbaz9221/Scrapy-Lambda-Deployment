from scrapy.cmdline import execute
def handler(event=None, context=None):
    cmdLine = []
    cmdLine.append("scrapy")
    cmdLine.append("runspider")
    cmdLine.append("spider.py")
    elements = event.get("elements",[])
    if elements is not None:
        for element in elements:
            cmdLine.append("-a")
            cmdLine.append(f"{element.get('fieldName')}={element.get('xpath',element.get('baseUrl'))}")
        execute(cmdLine)
        