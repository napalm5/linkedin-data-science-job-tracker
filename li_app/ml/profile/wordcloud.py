import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
from wordcloud import WordCloud

# TODO: split all this code into different modules


@st.cache
def train_ifidf_caching_wrapper(data: pd.DataFrame):
    '''
    Functional wrapper around the IF-IDF vectorizer that allows streamlit to 
    cache the results of the training.

    This caching changes the architecture of the code. Normally I would need to pass
    a Vectorizer to every profiling function. With streamlit cache I can just call this function.

    Should be rewritten in a smarter way, but it's low priority at the moment,
    since I do not plan on extending the functionalities of this module
    '''
    corpus = data.title.values

    # Here I should do more preprocessing. Will be added in the future
    #corpus = [c for c in corpus if len(c) > 2]
    
    # Train and use the vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', 
        ngram_range = (1,1),
        max_df = .6,
        min_df = .01
    ) # max_df and min_df are important, because I have a many-language corpus and I didn't do a preprocessing on stop-words
    # norm='l2') #could be useful
    vectorizer.fit(corpus)
        
    return vectorizer

@st.cache
def create_wordcloud(data: pd.DataFrame, text_color="hsl(0,100%, 1%)"):
    '''
    Takes as input dataframe with raw jobs, outputs wordcloud image (and tf-idf matrix?)

    TODO: Decompose it as a series of tasks performed by objects
    '''
    # TODO: double check that this makes sense
    vectorizer = train_ifidf_caching_wrapper(data)
    idf_vec = [1/v for v in vectorizer.idf_]
    feature_names = vectorizer.get_feature_names_out()
    freqs_dict = dict(zip(feature_names, idf_vec))

    # Create cloud of words
    wordcloud = WordCloud(
        background_color="white",
        width=1000, height=600,
    ).generate_from_frequencies(freqs_dict)

    color_func = lambda *args, **kwargs: text_color
    wordcloud.recolor(color_func = color_func)
    
    return wordcloud


#TODO: add heuristic to choose number of clusters
@st.cache
def cluster_jobs(data: pd.DataFrame, n_clusters=5):
    ''' 
    Vectorize job titles/descriptions, 

    TODO: Decompose it as a series of tasks performed by objects
    '''

    # Fetch and use the vectorizer
    corpus = data.title.values
    vectorizer = train_ifidf_caching_wrapper(data)
    feature_names = vectorizer.get_feature_names_out()
    tsidf_sparse_matrix = vectorizer.transform(corpus)
    feature_names = vectorizer.get_feature_names_out()

    #Format the results
    tsidf_matrix = tsidf_sparse_matrix.todense()
    tsidf_df = pd.DataFrame(tsidf_matrix, columns=feature_names)
    #tsidf_df = tsidf_df.transpose()
    tsidf_df.index = data.job_id

    # I do not need to preprocess this data, tsidf matrix is already scaled

    # Apply PCA to have a nb of features that do not distort Euclidean distance
    reducer = PCA(n_components=10)
    cluster_data = reducer.fit_transform(tsidf_df)

    # Cluster jobs
    # TODO: Select n_clusters based on some score, most probably silhouette score.
    clusterer = KMeans(n_clusters=n_clusters)
    clusterer.fit(cluster_data)
    labels = clusterer.predict(cluster_data)
    
    # Create data for visualization
    viz_reducer = PCA(n_components=2)
    viz_data = viz_reducer.fit_transform(tsidf_df)
    viz_data = pd.DataFrame(viz_data, index=data.job_id, columns=['x','y'])
    viz_data['label'] = labels

    return viz_data