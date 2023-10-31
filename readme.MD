# Scrapy AWS Lambda Deployment Code

This project is a web scraping application that utilizes Scrapy to extract data from web pages and store it in an AWS S3 bucket. It includes a Scrapy spider for data extraction, a Dockerfile for containerization, and configuration settings in `Conf.py`.

## Prerequisites

- Python 3.8
- Scrapy
- Docker

## Project Structure

- `app.py`: Lambda function code for running the Scrapy spider.
- `Spider.py`: The Scrapy spider for web data extraction.
- `Dockerfile`: Dockerfile for creating a containerized environment for the project.
- `Conf.py`: Configuration settings file for the project.

## Getting Started

1. **Install Dependencies**: Make sure you have Python 3.8 installed and install the required dependencies using pip:


2. **Configure Settings**: Customize the settings in `Conf.py` as needed for your specific web scraping and AWS S3 configurations.

3. **Run Locally**: You can test your Scrapy spider locally using the following command:

>scrapy runspider Spider.py

4. **Dockerize the Application**: You can containerize your project using Docker by building an image from the provided Dockerfile:

## Usage

- The `app.py` script is designed to be used in a Lambda function and can be triggered as an AWS Lambda function.
- The `Spider.py` script defines the Scrapy spider for web scraping. Customize it according to the specific website structure and data to be extracted.
- The `Dockerfile` is used to containerize the project, which can be deployed in various containerization platforms.
- `Conf.py` contains configuration settings for the project, such as S3 bucket and file names, field names, and XPath selectors.

## Contributing

If you'd like to contribute to this project, please follow these guidelines.