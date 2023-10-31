class ScrapySpiderSettings:
    """
    Scrapy Spider Settings

    This class defines essential settings for a Scrapy spider, including the AWS S3 bucket name, the name of the
    output JSON file, and lists of field names and corresponding XPath selectors for web data extraction.

    Attributes:
    -----------
    S3_BUCKET_NAME (str): The name of the AWS S3 bucket where extracted data will be stored.
    S3_FILE_NAME (str): The name of the JSON file in the S3 bucket for data storage.
    KEYS_FIELDS (list): A list of field names used to categorize and structure the extracted data.
    VALUE_SELECTORS (list): A list of corresponding XPath selectors to extract data for each field.

    Example Usage:
    --------------
    settings = ScrapySpiderSettings()
    s3_bucket = settings.S3_BUCKET_NAME
    s3_file = settings.S3_FILE_NAME
    fields = settings.KEYS_FIELDS
    selectors = settings.VALUE_SELECTORS
    """
    
    S3_BUCKET_NAME = "scrape-url-data"
    S3_FILE_NAME = "RecipeData.json"
    KEYS_FIELDS = ['field1', 'field2', ...]  # List of field names
    VALUE_SELECTORS = ['xpath1', 'xpath2', ...]  # List of corresponding XPaths

# Example Usage:
settings = ScrapySpiderSettings()

