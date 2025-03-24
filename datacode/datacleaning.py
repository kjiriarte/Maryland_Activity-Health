#cleaning + wrangling the data

import pandas as pd

#load in dataset
acres = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/MDAcres.csv")
#rename key to be able to merge datasets
acres.rename(columns={'Maryland County': 'Jurisdiction'}, inplace=True)

acres['Jurisdiction'] = acres['Jurisdiction'].str.replace('County', '', regex=True).str.strip()

#VARIABLES TO KEEP: JURISDICTION, TOTAL Publicly Owned, GRAND TOTAL Preserved, DNR State Land Inventory
#LPPRP Federal Park and Conservation Lands, LPPRP Local Parks and Recreation (incl. Local-Side POS)

#load in dataset
#keep all variables?? - would be good for analysis
eco = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/MDSocioeconomic.csv")
#rename key to be able to merge datasets - remove 'County from strings
eco.rename(columns={'Jurisdictions': 'Jurisdiction'}, inplace=True)
eco['Jurisdiction'] = eco['Jurisdiction'].str.replace('County', '', regex=True).str.strip()
eco['Jurisdiction'] = eco['Jurisdiction'].str.replace('city', 'City', regex=True).str.strip()

#load in dataset
#Keep all variables - remove anything older than 2019 to ensure most recent data is used

activity = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/MDPhysicalActivity.csv")
activity.rename(columns={'Race/ ethnicity': 'Race'}, inplace=True)
#remove unnecessary varaibles
activity = activity.drop('Measure', axis=1)
activity['Jurisdiction'] = activity['Jurisdiction'].str.replace('County', '', regex=True).str.strip()
activity['Jurisdiction'] = activity['Jurisdiction'].str.replace("Saint Mary's", "St. Mary's", regex=True).str.strip()
act = activity[activity['Year'] == 2019]


act = act.pivot(index=['Jurisdiction', 'Year'] ,columns='Race', values='Value')
act = act.reset_index()
act = act.drop(columns=['Race'], errors='ignore')

#print(act.columns.tolist())
#print(acres)

#load in dataset
parks = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/ParksData.csv")
#rename key to be able to merge datasets
parks.rename(columns={'County': 'Jurisdiction'}, inplace=True)
#parks = parks.pivot(index=['Jurisdiction'] ,columns=parks.count())

parks = parks.groupby('Jurisdiction').count().reset_index()
parks =parks.drop(parks.columns[[2]], axis=1)
parks.rename(columns={'Park Name': 'ParkCount'}, inplace=True)


#print (parks)



merged_df = parks.merge(acres, on='Jurisdiction', how='outer') \
               .merge(eco, on='Jurisdiction', how='outer') \
               .merge(act, on='Jurisdiction', how='outer')

mapdata = merged_df.drop([3, 20, 21])
mapdata = mapdata.drop(["Jurisdiction Code", "Maryland Region", "Best Available Data as of"], axis=1)
#print(merged_df)

#code file to work with for modeling + visualization
mapdata.to_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mapdata.csv", index=False)
#pd.merge()

