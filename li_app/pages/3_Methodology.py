import streamlit as st

st.title('Methodology')
st.sidebar.markdown("# Methodology")
'''
The idea behind the project is to give real-time snapshots of the ongoing trends in the data science job market.
To keep the project at a reasonable scale, I restrict the scope to profiles similar to mine. 
Please keep in mind that this analysis is still a work in progress, the process will probably be adjusted many times in the coming weeks.

## Dataset description
To do so, I collect a dataset containing every job posting advertized on LinkedIn the past weeks satisfying the criteria I usually emply in my job search queries:
Those are: mid to senior seniority, hybrid or remote working, and located in a country where I could speak the language. This means either Italy or one of the German-speaking countries in Europe.
I excluded the UK because of Visa problems. I update this dataset and relaunch the analysis every day.

For each job I collect the job title, the date of the posting, the company, the location of the company and in the future I plan to add a set of keywords from the job description.

Then I perform three different analyses, addressing the three most important questions that I had during my last job search


### 1) How many opportunities do I have?
First of all, I am interested in showing the average number of available job offers, and how this changes over time.
To do so, I aggregate the offers on a daily level, and count the number of jobs posted every day for the past few week.
I also use this historical dataset to train an anomaly detection algorithm, that will point out the days where there has been a spike in recruiting activity.
I had to choose an algorithm that could work around the important constraints in my dataset:
1. Few data points are available, because I can collect at most a few months (several hundred data points) of data.
2. Few computational resources. At the moment I am doing the computation directly on streamlit, which means I have limitations both in computational complexity and in computation time
       If necessary, I can circumvent this by moving the computation to a separate cloud process, and only use streamlit to deploy the model and visualize the results.
       However, the results so far do not justify the use of more complex models, so this change is not a priority at the moment.
3. Model needs to be interpretable. 
       Once again, I could solve the interpretation problem even with more complex models, but it would require a bigger amount of resources, which are not at the moment justified by the dataset.

Keeping these considerations in mind, and in particluar since I still have very few data points, I am only considering a very simple random walk model with drift.

I then perform the anomaly detection in an off-line way: first I train the model on the whole historical dataset, training it with a percentile objective.
Then I do an in-sample prediction, and I compute the expected 90-th percentile for the number of daily offers for every fay in the historical dataset.
Then, the actual number of job offers exceeds this thresholds, I flag it as an anomaly: that day the recruiters have been very busy!

This is of course a very naive methodology. I am currently not performing any checks on the reliability of the anomaly detection algorithm.
One of the high-priority items in the todo list of this project is to, instead of training the model on the whole dataset, perform a training with time-series cross-validation.
I will be then able to automatize both the reliability checks on the anomaly detection, and the model choosing process.

### 2) In which direction is the job market going?
Having studied how the market has behaved in the recent past, another important factor when job hunting are the future perspectives.
Are we moving towards an hiring freeze, and I should follow through with the good offer I received this week? Or are we heading to a quick growth, and I maybe could get a better opportunity in a couple weeks?  

This dataset allows me to make an educated guess for the number of job offers in the recent future.
To do so, I need a time-series forecasting model that satisfies all the constraints listed in the previous paragraph.
In fact, I am using the same model, but for this analysis I perform an out-of-sample forecasting for the 7 days after the current one.



### 3) What kind of opportunities are we talking about?
WIP
'''