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

	Country	Year	id	Subtype	Post	gdpc	FinStability	Freedom	PolitStability	Diff	...	lead_-10	lead_-9	lead_-8	lead_-7	lead_-6	lead_-5	lead_-4	lead_-3	lead_-2	lead_-1
0	United States	2002	1	0	1	38023.161114	25.6634	78.4	0.287509	0	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
8	United States	2003	1	0	1	39496.485875	25.6082	78.2	0.0812887	0	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
9	United States	2004	1	0	1	41712.801068	27.6959	78.7	-0.2313482	0	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
10	United States	2005	1	0	1	44114.747781	27.6230	79.9	-0.0586535	0	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
11	United States	2006	1	0	1	46298.731444	27.7233	81.2	0.4939433	0	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0
...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...	...
116	Brazil	2012	8	1	0	12370.024201	13.0293	57.9	0.0459616	-4	...	0.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0	0.0	0.0
117	Brazil	2013	8	1	0	12300.324882	12.5102	57.7	-0.2585533	-3	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0	0.0
118	Brazil	2014	8	1	0	12112.588206	12.8470	56.9	-0.0702901	-2	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	1.0	0.0
119	Brazil	2015	8	1	0	8814.000987	15.4336	56.6	-0.3314581	-1	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	1.0
7	Brazil	2016	8	1	1	8710.096690	15.4676	56.5	-0.3772054	0	...	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0	0.0

# saving the data 
olympics.to_csv("Downloads/ss154_data_collection/olympics.csv")

olympics_winter = olympics[olympics.Subtype==0]
olympics_summer = olympics[olympics.Subtype==1]

olympics_winter.to_csv("Downloads/ss154_data_collection/olympics_winter.csv")
olympics_summer.to_csv("Downloads/ss154_data_collection/olympics_summer.csv")

