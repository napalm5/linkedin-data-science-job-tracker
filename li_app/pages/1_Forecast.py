import streamlit as st

import matplotlib.pyplot as plt

st.set_page_config(page_title="Forecast", page_icon="📈")

st.markdown("# Forecast")
st.sidebar.header("Forecast")
st.write(
    """From the data presented in the introduction, I here try to predict 
    the volume of the job market in the next week."""
)

ts = st.session_state['ts'] 
forecast_results = st.session_state['forecast_results'] 

# TODO: put this in a function or in class of functions
#column names from statsforecast change depending on the model
forecast = forecast_results.forecast.set_index('ds')
forecast_column = [c for c in forecast.columns if \
    'hi-' not in c and \
    'lo-' not in c and \
    c not in ['unique_id','ds','y']\
    ][0]
forecast_highthresh_column = [c for c in forecast.columns if 'hi-' in c][0]
forecast_lowthresh_column = [c for c in forecast.columns if 'lo-' in c][0]

fig,ax = plt.subplots()
ax.scatter(ts.index,ts.values) # Main time series
ax.plot(ts.index, ts.values, linewidth=0.2,linestyle='-')# Interpolation
ax.scatter(
    forecast.index,
    forecast[forecast_column]
) # Forecast
# ax.fill_between(
#     x = forecast.index,
#     y1 = forecast[forecast_lowthresh_column],
#     y2 = forecast[forecast_highthresh_column],
#     alpha=0.5
# )
plt.xticks(rotation=45)
plt.ylabel('Number of jobs posted')
plt.xlabel('Date')
st.pyplot(fig)



# # Example of progress bar usage. Could be useful

# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")