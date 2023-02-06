import streamlit as st

import matplotlib.pyplot as plt
import matplotlib

from ml import profile as p

st.markdown("# Profiling")
st.sidebar.markdown("# Profiling")

# Env variables
data = st.session_state['data'] 
n_clusters = 5

# TODO: create classes instead of writing plot code here



'''
In addition to counting the number of jobs, looking at the linguistic features of their title and description can give us even more information about the job market.

For example, we might understand what kind of profiles are most in demand, or what skills are usually required to work as a data scientist.

Or, more interestingly, we can measure how much difference there is between job requirements in different fields. 
By interpreting the plots shown in this page, we can answer questions such as: should I specialize in a niche, or is it possible to be a generalist Data Scientist? How transferable will be the skills that I learn in a given job? 


### Most repeated keywords across all postings
'''

# Get global wordcloud
wordcloud = p.create_wordcloud(data)


fig, ax = plt.subplots()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(fig)


'''
### Segmentation of job offers

Most of LinkedIn job titles are informative enough to characterize the entire jobs. This plot is the 2-D projection of a clustering analysis performed on all the jobs considered, based on the linguistic features of their titles.

While the 2-D projection makes it difficult to visualize the separation between clusters, each cluster has its own distinctive properties. For example, one cluster might contain all the data engineering jobs, another one might contain all the management jobs, and so on.
'''
# Plot clustering of job posts
viz_data = p.cluster_jobs(data, n_clusters=n_clusters)
fig, ax = plt.subplots()
sc = ax.scatter(viz_data.x,viz_data.y,c=viz_data.label)
lines, labels = sc.legend_elements()
labels = [f'Cluster {l}' for l in labels]
ax.legend(lines, labels)
ax.set_xlabel('PCA - X')
ax.set_ylabel('PCA - Y')
st.pyplot(fig)

# Plot cloud of words separately for each cluster
# TODO: rewrite this nicely
'''
Characterizing clusters is in general a tricky task. 

You can get an idea about the properties of each job cluster by reproducing the cloud of words separately for each group. 

Which cluster would you like to look into?
'''

chosen_cluster = st.selectbox(
    '',
    range(n_clusters),
    label_visibility = 'collapsed'
)
main_keyword = ''

#st.write('This cluster contains job of the ',main_keyword,' category')
color = matplotlib.cm.get_cmap('viridis')((chosen_cluster)/(n_clusters-1))[:3]
color = tuple([int(c*255) for c in color])

cluster_wordcloud = p.create_wordcloud(
    data = data[viz_data.set_index(data.index).label == chosen_cluster],
    text_color = color)

fig, ax = plt.subplots()
plt.imshow(cluster_wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(fig)
