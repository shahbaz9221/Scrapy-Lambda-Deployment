FROM public.ecr.aws/lambda/python:3.8
COPY spider.py spider.py
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

CMD [ "app.handler" ]