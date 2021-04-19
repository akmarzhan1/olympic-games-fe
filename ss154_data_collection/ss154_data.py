import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np

#loading and cleaning the host countries file
olympics=pd.read_csv("Downloads/ss154_data_collection/data/olympic_hosts.csv")

olympics.drop(olympics[olympics.Type=='youthgames'].index, inplace=True)
olympics.drop(olympics[olympics.Year>=2018].index, inplace=True)
olympics.drop(olympics[olympics.Year<2002].index, inplace=True)

#dropping countries which hosted twice or more in the given time period
olympics = olympics.drop_duplicates(subset=['Country'], keep=False)

countries = olympics['Country'].to_numpy()

#generating ids
def generate_id(country):
    return list(countries).index(country)+1

olympics['id'] = olympics['Country'].apply(generate_id)

#specifying columns
olympics["Host"] = [1 for i in range(len(countries))]
olympics["Subtype"] = [1 for i in range(len(countries))]
olympics['Subtype'] = pd.get_dummies(olympics['Type'])
olympics = olympics[['Country', 'Year', 'id', 'Subtype', 'Host']]
olympics

#turning the dataset into panel data
years = np.arange(min(olympics['Year'].unique()), max(olympics['Year'].unique())+1, 1)

for country in countries:
    host_year = olympics[olympics.Country==country].Year.to_numpy()
    host_id = olympics[olympics.Country==country].id.to_numpy()[0]
    host_type = olympics[olympics.Country==country].Subtype.to_numpy()[0]

    for year in years:
        if host_year != year:
            olympics = olympics.append({'Country': country, 'Year': year, 'id': host_id, 'Subtype': host_type, 'Host': 0}, ignore_index=True)

#collecting needed info
gdp = pd.read_csv('Downloads/ss154_data_collection/data/gdp.csv')
olympics['gdp'] = [0 for i in range(len(olympics))]

fin = pd.read_csv('Downloads/ss154_data_collection/data/fin_data.csv')
olympics['FinStability'] = [0 for i in range(len(olympics))]

freedom = pd.read_csv('Downloads/ss154_data_collection/data/freedom.csv')
olympics['Freedom'] = [0 for i in range(len(olympics))]

polit = pd.read_csv('Downloads/ss154_data_collection/data/polit.csv')
olympics['PolitStability'] = [0 for i in range(len(olympics))]

pop = pd.read_csv('Downloads/ss154_data_collection/data/pop.csv')
olympics['Population'] = [0 for i in range(len(olympics))]


#gdp
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['gdp'][idx] = gdp[gdp['Country Name']==country][str(year)].to_numpy()[0]
        
#financial stability
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['FinStability'][idx] = fin[(fin['country']==country)&(fin['year']==year)]['gfddsi01'].to_numpy()[0]

#freedom index
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['Freedom'][idx] = freedom[(freedom['Name']==country)&(freedom['Index Year']==year)]['Overall Score'].to_numpy()[0]

#population
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['Population'][idx] = pop[pop['Country Name']==country][str(year)].to_numpy()[0]
        
#political stability
for country in countries:
    for year in years:
        idx = olympics.loc[(olympics.Country==country) & (olympics.Year==year)].index
        olympics['PolitStability'][idx] = polit[(polit['Country Name']==country)&(polit['Series Name']=='Political Stability and Absence of Violence/Terrorism: Estimate')]['{0} [YR{0}]'.format(year)].to_numpy()[0]

#calculating the difference between the hosting year and the current year for each observation
diff = []
olympics['Diff']= [0 for i in range(len(olympics))]
indices = olympics.index.to_numpy()
for idx in indices:
    host_year = olympics[(olympics.Country == olympics.iloc[idx].Country) & (olympics.Host==1)].Year.to_numpy()[0]
    if olympics.iloc[idx].Host==1:
        olympics['Diff'][idx]=0
    else:
        olympics['Diff'][idx]=olympics.iloc[idx].Year - host_year
        
#encoding the differences to get the lags and leads
one_hot = pd.get_dummies(olympics[olympics.Diff<0].Diff, prefix='lead')
two_hot = pd.get_dummies(olympics[olympics.Diff>0].Diff, prefix='lag')
olympics = pd.concat([olympics, one_hot, two_hot], axis=1)
olympics = olympics.fillna(0)

#sorting the values 
olympics = olympics.sort_values(by=['id', 'Year'])

#saving the csv files
olympics.to_csv("Downloads/ss154_data_collection/olympics.csv")

olympics_winter = olympics[olympics.Subtype==0]
olympics_summer = olympics[olympics.Subtype==1]

olympics_winter.to_csv("Downloads/ss154_data_collection/olympics_winter.csv")
olympics_summer.to_csv("Downloads/ss154_data_collection/olympics_summer.csv")
