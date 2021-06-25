from pprint import pprint
from sys import flags
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
try:
    if choices == 'Total Report':
        d = st.date_input(
            "Would you pick any date ?",
            datetime.date(year, month, dd)
            )

        st.write('Total data for the entire world as of', d, ':mask:')
        df = totals(d)
        df
        
        total_confirmed = df["confirmed"].sum()
        total_deaths = df["deaths"].sum()
        total_recovered = df["recovered"].sum()
        total_active = df["active"].sum()

    ## Funnel Chart
        fig = go.Figure(go.Funnel(
            x = [total_confirmed,total_deaths,total_recovered,total_active],
            y=["Confirmed Cases", "Deaths", "Recovered", "Active"],
            textposition = "inside",
            textinfo = "value+percent initial",
            opacity = 0.65, 
            marker = {"color": ["darkred", "red", "green", "yellow", "silver"],
            "line": {"width": [4, 2, 2, 3, 1, 1], "color": ["wheat", "wheat", "blue", "wheat", "wheat"]}},
            connector = {"line": {"color": "royalblue", "dash": "dot", "width": 3}}))
        fig.update_layout(width=1000,height=600,title='Total World Data as of ' + str(d))
        st.plotly_chart(fig)
        
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
        report_date = st.date_input(
            "Do you want to pick any date ?",
            datetime.date(year, month, dd)
        )
        iso_code=st.selectbox(
            'Enter ISO code you"re interested in',
            df['iso']
        )
        st.write('Total data for', iso_code, 'as of', report_date, ':mask:')
        df = reports(report_date,iso_code)
        st.write(df)
        
        total_confirmed = df["confirmed"].sum()
        total_deaths = df["deaths"].sum()
        total_recovered = df["recovered"].sum()
        total_active = df["active"].sum()


        # Create 2 Columns 
        col1, col2 = st.beta_columns(2)
        fig=px.bar(df,x='province',y=['confirmed'],template='xgridoff',title='Covid Confirmed Cases ' +'<b>'+ str(total_confirmed))
        col1.write(fig)

        fig=go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df['province'],y=df['deaths'],mode='lines+markers',line=dict(color='firebrick', width=2),
                ))
        fig.update_layout(title='Number of Covid Deaths ' +'<b>'+str(total_deaths))
        col2.write(fig)
        
        # Create 2 Columns 
        col3, col4 = st.beta_columns(2)
        fig = px.pie(
                df,names='province',values='recovered',title='Covid Recovery Graph ' +'<b>'+ str(total_recovered)
                )
        fig.update_layout(width=600,height=800)
        col3.write(fig)

        df = df[df['active']>0]
        fig = px.scatter(
                df,x='province',y='active',size="active",color="province",
                hover_name="province",title='Covid Active Cases Graph ' + '<b>'+str(total_active)
                )
        fig.update_layout(width=800,height=600)
        col4.write(fig)

        #col5, col6 = st.beta_columns(2)
        fig=px.bar(df,x='province',y=['confirmed','active','recovered','deaths'],template='xgridoff',
        title='Total Confirmed Cases ' +'<b>'+ str(total_confirmed) + '</b>''<br>' +
        'Total Deaths ' +'<b>'+ str(total_deaths) + '</b>''<br>' +
        'Total Recovered cases ' +'<b>'+ str(total_recovered) +'</b>' '<br>' +
        'Total Active cases ' +'<b>'+ str(total_active))
        fig.update_layout(width=1000,height=550)
        st.write(fig) 

        lat = df['lat'].astype(float)
        lon=df['long'].astype(float)

        fig1 = px.scatter_mapbox(
            
            df,lat=lat,lon=lon,
            color='confirmed', size="confirmed",
            hover_name='province',
            hover_data=['confirmed','deaths','recovered','active'],
            color_continuous_scale=px.colors.sequential.Viridis, zoom=3,
            color_discrete_map={},
                    #animation_frame='province',
            mapbox_style="carto-positron",
        )
        fig.update_layout(width=1000,height=500)
        st.write(fig1)
except:
    'Data will be update 12 am today, meahwhile have a', ':beer:'
