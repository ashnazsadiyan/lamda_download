FROM public.ecr.aws/lambda/python:3.11

RUN yum install -y java-1.8.0-openjdk

COPY nltk_docks .

# Create a directory for data
RUN mkdir /tmp/data



# Set the TRANSFORMERS_CACHE environment variable
ENV TRANSFORMERS_CACHE "/tmp/data"

# Copy requirements.txt and install the required packages
COPY requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy app.py
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD for the Lambda function
CMD [ "app.handler" ]

