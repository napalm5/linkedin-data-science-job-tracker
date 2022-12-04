FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code and its dependencies
# This looks a bit hacky, but cloning the repo is unsafe
# I should research best practice for this 
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
ADD io ${LAMBDA_TASK_ROOT}/io
ADD scrape ${LAMBDA_TASK_ROOT}/scrape

# Set environment variables
# These are the secrets that will be overwritten by AWS conf, for security reasons
ENV aws_access_key_id=xxx
ENV aws_secret_access_key=yyy
ENV LI_AT_COOKIE=zzz

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ] 