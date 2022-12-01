import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Streamlit settings #
st.set_page_config(layout='wide')

st.header('HELLO')


# get data
file_url = 'https://raw.githubusercontent.com/danm91/reboot_lbg/code/emissions.csv'
df = pd.read_csv(file_url)
df = df.set_index('timestamp')

#fake data
df1 = df.copy()
df1.energy_consumed = df1.energy_consumed.apply(lambda x:x if x < df1.energy_consumed.mean() else x*np.random.uniform(0.7,0.8))
df1.project_name = 'optimal'

merged_ = pd.concat([df[['project_name','energy_consumed']],df1[['project_name','energy_consumed']]],axis=0)

fig=px.line(merged_, x=merged_.index, y='energy_consumed', color='project_name')

st.plotly_chart(fig)