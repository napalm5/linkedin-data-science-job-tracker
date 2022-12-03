import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters

from datetime import datetime

import boto3

#LI_AT_COOKIE="AQEDASSauyICe5R9AAABg5z5DJMAAAGE4dw_nE0AV_A__Y853wtXZ2NmdgcaamBvPfvmX4G1DVj69UG3aHM1FbEyoBecWAlcV5dXAVm2zXuSfYUkxUozmCeHAaPTHd0QsK5U3PMyujgc5_M5cHVtTnpW"


# Change root logger level (default is WARN)
logging.basicConfig(level = logging.INFO)

all_jobs = []

def event_to_dict(data_event):
    fields = ['job_id','date','title','company','location']
    data = {field : getattr(data_event,field) for field in fields}
    if data['date'] == '': 
        data['date'] = datetime.today().strftime('%Y-%m-%d')
        print('Date missing!')
    data['year'] = datetime.today().year
    data['month'] = datetime.today().month  

    return data

# Fired once for each successfully processed job
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.date)
    all_jobs.append(event_to_dict(data))

# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
  print('[ON_METRICS]', str(metrics))

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')

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
            limit=100000,
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

db = boto3.resource('dynamodb')
table = db.Table('LinkedInDSJobs')

with table.batch_writer() as batch:
    for job_data in all_jobs:
        batch.put_item(
            Item=job_data
            )

#table.put_item(Item=job_data)

