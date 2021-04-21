#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
import numpy as np
warnings.filterwarnings('ignore')
import pandas as pd
olympics=pd.read_csv("Downloads/ss154_data_collection/data/olympic_hosts.csv")

#dropping the unnecessary rows
olympics.drop(olympics[olympics.Type=='youthgames'].index, inplace=True)
olympics.drop(olympics[olympics.Year>=2018].index, inplace=True)
olympics.drop(olympics[olympics.Year<2002].index, inplace=True)

#dropping those treated more than once
olympics = olympics.drop_duplicates(subset=['Country'], keep=False)

countries = olympics['Country'].to_numpy()

#generating ids
def generate_id(country):
    return list(countries).index(country)+1

olympics['id'] = olympics['Country'].apply(generate_id)

#showing the needed columns
olympics["Post"] = [1 for i in range(len(countries))]
olympics["Subtype"] = [1 for i in range(len(countries))]
olympics['Subtype'] = pd.get_dummies(olympics['Type'])
olympics = olympics[['Country', 'Year', 'id', 'Subtype', 'Post']]

#adding the panel data for different years
years = np.arange(min(olympics['Year'].unique()), max(olympics['Year'].unique())+1, 1)

for country in countries:
    host_year = olympics[olympics.Country==country].Year.to_numpy()
    host_id = olympics[olympics.Country==country].id.to_numpy()[0]
    host_type = olympics[olympics.Country==country].Subtype.to_numpy()[0]

    for year in years:
        if host_year > year:
            olympics = olympics.append({'Country': country, 'Year': year, 'id': host_id, 'Subtype': host_type, 'Post': 0}, ignore_index=True)

        elif host_year < year:
            olympics = olympics.append({'Country': country, 'Year': year, 'id': host_id, 'Subtype': host_type, 'Post': 1}, ignore_index=True)

        else:
            continue
            
#adding the needed variables 
gdpc = pd.read_csv('Downloads/ss154_data_collection/data/gdpc.csv')
olympics['gdpc'] = [0 for i in range(len(olympics))]

fin = pd.read_csv('Downloads/ss154_data_collection/data/fin_data.csv')
olympics['FinStability'] = [0 for i in range(len(olympics))]

freedom = pd.read_csv('Downloads/ss154_data_collection/data/freedom.csv')
olympics['Freedom'] = [0 for i in range(len(olympics))]

polit = pd.read_csv('Downloads/ss154_data_collection/data/polit.csv')
olympics['PolitStability'] = [0 for i in range(len(olympics))]

for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['gdpc'][idx] = gdpc[gdpc['Country Name']==country][str(year)].to_numpy()[0]
        
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['FinStability'][idx] = fin[(fin['country']==country)&(fin['year']==year)]['gfddsi01'].to_numpy()[0]
        
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['Freedom'][idx] = freedom[(freedom['Name']==country)&(freedom['Index Year']==year)]['Overall Score'].to_numpy()[0]

for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['PolitStability'][idx] = polit[(polit['Country Name']==country)&(polit['Series Name']=='Political Stability and Absence of Violence/Terrorism: Estimate')]['{0} [YR{0}]'.format(year)].to_numpy()[0]
        
#adding the lags and leads
diff = []
olympics['Diff']= [0 for i in range(len(olympics))]
indices = olympics.index.to_numpy()
for idx in indices:
    host_year = olympics[(olympics.Country == olympics.iloc[idx].Country) & (olympics.Post==1)].Year.to_numpy()[0]
    if olympics.iloc[idx].Post==1:
        olympics['Diff'][idx]=0
    else:
        olympics['Diff'][idx]=olympics.iloc[idx].Year - host_year

#adding dummy
one_hot = pd.get_dummies(olympics[olympics.Diff<0].Diff, prefix='lead')
two_hot = pd.get_dummies(olympics[olympics.Diff>0].Diff, prefix='lag')
olympics = pd.concat([olympics, one_hot, two_hot], axis=1)
olympics = olympics.fillna(0)

olympics = olympics.sort_values(by=['id', 'Year'])
olympics


# In[2]:


# saving the data 
olympics.to_csv("Downloads/ss154_data_collection/olympics.csv")

olympics_winter = olympics[olympics.Subtype==0]
olympics_summer = olympics[olympics.Subtype==1]

olympics_winter.to_csv("Downloads/ss154_data_collection/olympics_winter.csv")
olympics_summer.to_csv("Downloads/ss154_data_collection/olympics_summer.csv")

