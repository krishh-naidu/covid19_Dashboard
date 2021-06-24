from pprint import pprint
import streamlit as st
import datetime
from datetime import date,timedelta
import pandas as pd
#from traitlets.traitlets import default
from covid_dashboard_data import totals,provinces,regions,reports
import plotly.express as px
import plotly.graph_objects as go

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

today = date.today() - timedelta(days=1)
year = int(today.strftime('%Y'))
month = int(today.strftime('%m'))
dd = int(today.strftime('%d'))

options = ['Select one from below','Total Report','Provinces','Regions','Reports']
choices = st.sidebar.selectbox('Select options from below',
    options
)

if choices == 'Total Report':
    d = st.date_input(
        "Would you pick any date ?",
        datetime.date(year, month, dd)
        )

    st.write('Total data for the entire world as of', d, ':mask:')
    df = totals(d)
    st.write(df)

    fig = px.line(df,y=['confirmed','deaths','active','recovered'])
    st.write(fig)

if choices == 'Provinces':
    df = regions()
    iso_code=st.selectbox(
        'Enter ISO code you"re interested in',
        df['iso']
        )

    st.write(provinces(iso_code))

if choices == 'Regions':

    st.write(regions())

if choices == 'Reports':
    df = regions()
    d = st.date_input(
        "Would you pick any date ?",
        datetime.date(year, month, dd)
    )
    iso_code=st.selectbox(
        'Enter ISO code you"re interested in',
        df['iso']
    )
    st.write('Total data for', iso_code, 'as of', d, ':mask:')
    df = reports(d,iso_code)
    st.write(df)
    col1, col2 = st.beta_columns(2)
    fig=px.bar(df,x='province',y=['confirmed'],template='xgridoff',title='Covid Confirmed Cases Chart')
    col1.write(fig)

    fig=go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df['province'],y=df['deaths'],mode='lines+markers',line=dict(color='firebrick', width=2),
            ))
    fig.update_layout(title='Number of Covid Deaths')
    col2.write(fig)
    
    col3, col4 = st.beta_columns(2)
    fig = px.pie(
            df,names='province',values='recovered',title='Covid Recovery Graph'
            )
    fig.update_layout(width=600,height=800)
    col3.write(fig)
    df = df[df['active']>0]
    fig = px.scatter(
            df,x='province',y='active',size="active",color="province",
            hover_name="province",title='Covid Active Cases Graph'
            )
    fig.update_layout(width=800,height=600)
    col4.write(fig)

