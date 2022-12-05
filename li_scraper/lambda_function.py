import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters
from scrape import handlers as h
import export as io

from datetime import datetime

import json
import os
import sys

# In local, secrets are also written in  ./.secret

def lambda_handler(event,context):#event):#,context):
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

    scraper.on(Events.DATA, h.on_data)
    scraper.on(Events.ERROR, h.on_error)
    scraper.on(Events.END, h.on_end)

    queries = [
        Query(
            query='Data Science',
            options=QueryOptions(
                locations=['Italy','Germany','Austria','Switzerland','France','UK'],            
                apply_link = False,  # Try to extract apply link (easy applies are skipped). Default to False.
                limit=1000000, #A limitation could cause huge biases in the analysis
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.DAY,
                    type=[TypeFilters.FULL_TIME],
                    experience=[
                        ExperienceLevelFilters.ENTRY_LEVEL,
                        ExperienceLevelFilters.ASSOCIATE,
                        ExperienceLevelFilters.MID_SENIOR,
                        ExperienceLevelFilters.DIRECTOR
                        ],                
                )
            )
        ),
    ]

    scraper.run(queries)

    # Write results to DynamoDB
    outputter = io.DynamoDBExport(table='LinkedInDSJobs')
    outputter.put(h.all_jobs)
    
    return {
        'statusCode' : 200,
        'body' : json.dumps(f'Successfully scraped {len(h.all_jobs)} jobs')

    }
