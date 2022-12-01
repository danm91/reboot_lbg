import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pyodbc


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

fig0=px.line(merged_, x=merged_.index, y='energy_consumed', color='project_name')

st.plotly_chart(fig0)

# projects

st.header('Project tracker')
st.text('Some lorem ipsus stuff here...?')

# fake project data
df = pd.read_csv('emissions_sector.csv')

# make imaginary timescale - change to 12 month period. take 2000-2011
df = df.loc[lambda x:((x.Year>1999) & (x.Year < 2012)),:]
# total 
df['total'] = df.iloc[:,3:].sum(axis=1)

# get county codes
grpd = df.groupby('Code').agg(total_emissions = ('total','sum')).sort_values('total_emissions',ascending = False)
project_codes = grpd.head(10).index.to_list()

cols = ['Code', 'Year', 'total']
x_ = df.loc[lambda x:x.Code.isin(project_codes), cols]
x_['cumsum']=0
for country in x_['Code']:
    x_.loc[lambda x:x.Code == country, 'cumsum'] = x_.loc[lambda x:x['Code'] == country,'total'].cumsum()
    
#map dict
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
countries = x_.Year.value_counts().index
month_map = dict(zip(countries,months))
x_.Year = x_.Year.map(month_map)

proj_dict = dict(zip(x_.Code.value_counts().index.to_list(), [f'project_{x}' for x in range(1,11)]))
x_.Code = x_.Code.map(proj_dict)

x_['cumsum'] = x_['cumsum']/10000000

x_ = x_.rename(columns={'Code':'Project'})
fig1 = px.line(x_, x='Year', y='cumsum', color='Project')
fig1.update_yaxes(title='Carbon Emissions (kg)')
fig1.update_xaxes(title='Month')
fig1.update_layout()
st.plotly_chart(fig1)


server = 'reboot.database.windows.net'
database = 'codecarbon'
username = 'azureuser'
password = 'R3b00t123'


cnxn = pyodbc.connect(f'DRIVER={Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT * from emissions"
df_ = pd.read_sql(query, cnxn)

st.table(df_)