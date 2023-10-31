# Use the AWS Lambda Python 3.8 base image
FROM public.ecr.aws/lambda/python:3.8

# Copy your Python script and app code
COPY spider.py spider.py
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./

# Install the required dependencies
RUN python -m pip install -r requirements.txt

# Specify the Lambda handler
CMD [ "app.handler" ]
