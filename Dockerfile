FROM public.ecr.aws/lambda/python:3.11


RUN yum install -y java-1.8.0-openjdk

# Create a directory for data
RUN mkdir /tmp/data

COPY tmp/* /tmp

# Set the TRANSFORMERS_CACHE environment variable
ENV TRANSFORMERS_CACHE "/tmp/data"

# Copy requirements.txt and install the required packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy app.py
COPY app.py ${LAMBDA_TASK_ROOT}
#COPY tmp/vader_lexicon.txt .

# Set the CMD for the Lambda function
CMD [ "app.handler" ]

