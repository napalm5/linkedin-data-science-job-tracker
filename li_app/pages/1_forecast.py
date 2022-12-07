import streamlit as st

import matplotlib.pyplot as plt

st.set_page_config(page_title="Forecast", page_icon="📈")

st.markdown("# Forecast")
st.sidebar.header("Forecast")
st.write(
    """From the data presented in the introduction, I here try to predict 
    the volume of the job market in the next week."""
)

raw_data = st.session_state['raw_data']
data = st.session_state['data'] 


fig,ax = plt.subplots()
data.groupby('date').size().plot(ax=ax)
plt.xlabel('Number of jobs posted')
plt.ylabel('Date')
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