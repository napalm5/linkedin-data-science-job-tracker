FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
# Very bad practice: I should fork the repo of the python package and install my patched version
# But I already spent 12 hours just on finding the bug
RUN sed -i '281s/No jobs found, skip/No job container found in page/' /var/task/linkedin_jobs_scraper/strategies/authenticated_strategy.py
RUN sed -i '282s/return/# return/' /var/task/linkedin_jobs_scraper/strategies/authenticated_strategy.py

# Install chromedriver and chromium
# https://github.com/umihico/docker-selenium-lambda
# https://maartenbruntink.nl/blog/2022/09/19/running-selenium-and-chrome-in-lambda-to-build-a-simple-scraper/
# https://github.com/aws-samples/serverless-ui-testing-using-selenium/blob/main/Dockerfile #Best one
# TODO: Not all of these packages are necessary, remove the excess
RUN yum install xz atk cups-libs gtk3 libXcomposite alsa-lib tar \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel unzip bzip2 -y 

#RUN yum install unzip atk at-spi2-atk gtk3 cups-libs pango libdrm \ 
#    libXcomposite libXcursor libXdamage libXext libXtst libXt \
#    libXrandr libXScrnSaver alsa-lib -y

#COPY --from=build /opt/chrome-linux /opt/chrome
#COPY --from=build /opt/chromedriver /opt/

# Copy function code and its dependencies
# This looks a bit hacky, but cloning the repo is unsafe
# I should research best practice for this 
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY export ${LAMBDA_TASK_ROOT}/export
COPY scrape ${LAMBDA_TASK_ROOT}/scrape
COPY resources ${LAMBDA_TASK_ROOT}/resources

#RUN chmod +x ${LAMBDA_TASK_ROOT}/resources/install-chrome.sh
#RUN ${LAMBDA_TASK_ROOT}/resources/install-chrome.sh
RUN cp ${LAMBDA_TASK_ROOT}/resources/install-chrome-aws.sh /tmp/install-chrome-aws.sh
RUN chmod +x /tmp/install-chrome-aws.sh
RUN /usr/bin/bash /tmp/install-chrome-aws.sh

# Set environment variables
#ENV PATH="${PATH}:${LAMBDA_TASK_ROOT}/resources"
ENV PATH="/opt/chrome:/opt/chromedriver:${PATH}"
# These are the secrets that will be read in the different authentication steps
# Apart from security concerns, they cannot be used in Lambda, need to use AWS Role settings
#ENV AWS_ACCESS_KEY_ID=xxx
#ENV AWS_SECRET_ACCESS_KEY=yyy
#ENV AWS_DEFAULT_REGION=zzz
#ENV LI_AT_COOKIE=zzz

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ] 
# CMD [ "filename.anyfunc" ] 
