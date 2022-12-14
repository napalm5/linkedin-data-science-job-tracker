from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from datetime import datetime

# Very bad use of global variables, need to find a way to catch output from on_data()
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
    # This attribution of year and month could cause problem, because missing date will be filled with a bfill
    # But there should not be a difference of more than a month between the two methods
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
