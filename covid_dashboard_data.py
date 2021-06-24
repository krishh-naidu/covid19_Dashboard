import json
import requests
import pandas as pd
from pprint import pp, pprint

r = requests.get('https://covid-api.mmediagroup.fr/v1/cases')

response = json.loads(r.text)

#pprint(response.keys())

country_details=[]
keys = response.keys()

for key in keys:
    country_details.append(response[key]['All'])

data_tuples=list(zip(country_details))
df = pd.DataFrame(data_tuples,columns=['response'])

# breaking disctionary of columns into separate columns and create dataframe
df = pd.concat([df['response'].apply(pd.Series), df.drop('response', axis = 1)], axis = 1)
df = df[['country','population','sq_km_area','life_expectancy','continent','abbreviation','location','iso','capital_city',
'lat','long','confirmed','recovered','deaths']]



### John Hopkins Covid 19 Data
### Totals
headers = {
    'x-rapidapi-key': "facd6a6492msh12a82222a9dd6fdp10a786jsnc9bb4160c599",
    'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com"
    }

def totals(date):
    url = "https://covid-19-statistics.p.rapidapi.com/reports/total"

    querystring = {"date":date}

    total_response = requests.request("GET", url, headers=headers, params=querystring)

    total_resp = json.loads(total_response.text)

    totals=[]
    totals.append(total_resp['data'])
    data_tuples=list(zip(totals))
    df = pd.DataFrame(data_tuples,columns=['totals'])
    df = pd.concat([df['totals'].apply(pd.Series), df.drop('totals', axis = 1)], axis = 1)

    return df
    


### PROVINCES
def provinces(country):
    url = "https://covid-19-statistics.p.rapidapi.com/provinces"

    querystring = {"iso":country}
    provinces_response = requests.request("GET", url, headers=headers, params=querystring)

    provinces_resp = json.loads(provinces_response.text)
    iso=[]
    name=[]
    province=[]
    lat=[]
    long=[]

    for i in range(len(provinces_resp['data'])):
        iso.append(provinces_resp['data'][i]['iso'])
        name.append(provinces_resp['data'][i]['name'])
        province.append(provinces_resp['data'][i]['province'])
        lat.append(provinces_resp['data'][i]['lat'])
        long.append(provinces_resp['data'][i]['long'])
    
    data_tuples=list(zip(iso,name,province,lat,long))
    df = pd.DataFrame(data_tuples,columns=['iso','name','province','lat','lon'])

    return df


# REGIONS
def regions():
    url = "https://covid-19-statistics.p.rapidapi.com/regions"
    regions_response = requests.request("GET", url, headers=headers)
    regions_resp = json.loads(regions_response.text)
    iso=[]
    name=[]

    for i in range(len(regions_resp['data'])):
        iso.append(regions_resp['data'][i]['iso'])
        name.append(regions_resp['data'][i]['name'])
        
    
    data_tuples=list(zip(iso,name))
    df = pd.DataFrame(data_tuples,columns=['iso','name'])

    return df


# REPORTS
def reports(date,iso_code):
    url = "https://covid-19-statistics.p.rapidapi.com/reports"

    #querystring = {"date":"2021-06-22","q":"Alabama","iso":"USA"}
    querystring = {"date":date,"iso":iso_code}
    reports_response = requests.request("GET", url, headers=headers, params=querystring)
    reports_resp = json.loads(reports_response.text)
    #data = reports_resp(['data'][0]['region']['cities'])
    #pprint(data)
    #new_df = pd.DataFrame(data)
    #new_df
    data_tuples=list(zip(reports_resp['data']))
    
    df = pd.DataFrame(data_tuples,columns=['totals'])
    df = pd.concat([df['totals'].apply(pd.Series), df.drop('totals', axis = 1)], axis = 1)
    df = pd.concat([df['region'].apply(pd.Series), df.drop('region', axis = 1)], axis = 1)
    #df = pd.concat([df['cities'].apply(pd.Series), df.drop('cities', axis = 1)], axis = 1)
    #df = pd.concat([df[0].apply(pd.Series), df.drop(0, axis = 1)], axis = 1)

    #if iso_code=='USA':
     #   df = pd.DataFrame(data_tuples,columns=['totals'])
      #  df = pd.concat([df['totals'].apply(pd.Series), df.drop('totals', axis = 1)], axis = 1)
       # df = pd.concat([df['region'].apply(pd.Series), df.drop('region', axis = 1)], axis = 1)
        #df = pd.concat([df['cities'].apply(pd.Series), df.drop('cities', axis = 1)], axis = 1)
        #pprint(len(df['cities']))
        #df = pd.concat([df[0].apply(pd.Series), df.drop(0, axis = 1)], axis = 1)
        #print(len([df['cities']]))
    #else:
     #   df = pd.DataFrame(data_tuples,columns=['totals'])
      #  df = pd.concat([df['totals'].apply(pd.Series), df.drop('totals', axis = 1)], axis = 1)
       # df = pd.concat([df['region'].apply(pd.Series), df.drop('region', axis = 1)], axis = 1)
    return df

#print(reports('2021-06-01','USA'))