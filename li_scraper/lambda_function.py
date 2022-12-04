import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters
#import handlers as h

from datetime import datetime

import boto3
import json
import os
import sys

#LI_AT_COOKIE="AQEDASSauyICe5R9AAABg5z5DJMAAAGE4dw_nE0AV_A__Y853wtXZ2NmdgcaamBvPfvmX4G1DVj69UG3aHM1FbEyoBecWAlcV5dXAVm2zXuSfYUkxUozmCeHAaPTHd0QsK5U3PMyujgc5_M5cHVtTnpW"

# Bad use of global variables, need to find a way to catch output from on_data()
all_jobs = []


def event_to_dict(data_event):
    '''
    Exctract relevant information from the whole job posting.
    This could be either turned into a class, or merged into the linkedin-scraper package
    '''
    fields = ['job_id','date','title','company','location']
    data = {field : getattr(data_event,field) for field in fields}
    if data['date'] == '': 
        #data['date'] = datetime.today().strftime('%Y-%m-%d')
        print('Date missing!')
    data['year'] = datetime.today().year
    data['month'] = datetime.today().month  

    return data

def on_data(data: EventData):
    # Fired once for each successfully processed job
    print('[ON_DATA]', data.title, data.company, data.date)
    all_jobs.append(event_to_dict(data))

def on_metrics(metrics: EventMetrics):
    # Fired once for each page (25 jobs)
    print('[ON_METRICS]', str(metrics))

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')


def lambda_handler(event,context):
    # Change root logger level (default is WARN)
    logging.basicConfig(level = logging.INFO)

    # Scraper gets his LinkedIn authentication from env variable LI_AT_COOKIE
    scraper = LinkedinScraper(
        chrome_executable_path=None, # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver) 
        chrome_options=None,  # Custom Chrome options here
        headless=True,  # Overrides headless mode only if chrome_options is None
        max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
        slow_mo=5.,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
        page_load_timeout=20  # Page load timeout (in seconds)    
    )

    scraper.on(Events.DATA, on_data)
    scraper.on(Events.ERROR, on_error)
    scraper.on(Events.END, on_end)

    queries = [
        Query(
            query='Data Science',
            options=QueryOptions(
                locations=['Italy'],            
                apply_link = False,  # Try to extract apply link (easy applies are skipped). Default to False.
                limit=5,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.DAY,
                    type=[TypeFilters.FULL_TIME],
                    experience=None,                
                )
            )
        ),
    ]

    scraper.run(queries)

    # Boto should get his credentials from the env variables:
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY 
    db = boto3.resource('dynamodb')
    table = db.Table('LinkedInDSJobs')

    with table.batch_writer() as batch:
        for job_data in all_jobs:
            batch.put_item(
                Item=job_data
                )

    #table.put_item(Item=job_data)
    return {
        'statusCode' : 200,
        'body' : json.dumps(f'Successfully scraped {len(all_jobs)} jobs')
    }
