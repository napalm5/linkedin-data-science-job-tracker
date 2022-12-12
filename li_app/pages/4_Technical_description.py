import streamlit as st

st.title('Technical description')
st.sidebar.markdown("# Technical description")

#Created from
#https://www.figma.com/file/T62NQQ9W1aaHbzX2TABzyD/Tech-Stack-Diagram-(Copy)?node-id=0%3A1&t=j0W8735wdmMG6Pjh-0
st.image('./li_app/assets/Tech_Stack_Diagram.png')

'''
The architecture of this application is divided into two parts:

### Scraping
The first is the scraping process, where a small scraping function is packaged with all its dependencies into a Docker container, it is deployed on AWS Lamda and scheduled for execution every day at 22:00 UTC+1 (my current timezone).
The function scrapes all the jobs it can find for the current date, and saves an object containing the attributes of the job into a DynamoDB table.

### Computation and deployment
The second part covers both the computation and the deployment of the data analysis, and it is performed by the deployment platform.
Inside a Streamlit app, deployed on the Streamlit cloud, I fetch the table containing all historical job postings, manipulate it to obtain the data I want to visualize (time series, vector representations and so on), and I serve the visualization on the resulting website.

For bigger projects this workflow would not be possible, as the resources on the deployment platform are limited, and long computation times would delay too much the loading of the web application.
In this case, it would be needed to extract the computation part and deploy it on another cloud computation instance, like I am doing for the scraping part, creating a three-parts architecture.
For the purposes of this project, I prefer to keep both the developement time and the complexity of the architecture low (and also the prices of the cloud services).
I then choose to both keep the dataset small (by filtering the job postings), and the computational costs low (by choosing lightweight models and employing the caching functionalities of Streamlit).

In particular, I chose to do the time series analysis with the Python library statsforecast, and the NLP analysis with scikit-learn.
'''
