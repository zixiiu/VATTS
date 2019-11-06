import pandas as pd
import numpy as np

### Yelp location could be messed up because some of the restaurants have extra information about location
def merge_location_Yelp(Yelp):
    for i,each_line in Yelp.iterrows():
        if each_line.location__address2 == each_line.location__address2:
            each_line.location__address1 = each_line.location__address1 + ', ' + each_line.location__address2
            Yelp.at[i,'location__address1'] = each_line.location__address1
        if each_line.location__address3 == each_line.location__address3:
            each_line.location__address1 = each_line.location__address1 + ', ' + each_line.location__address3
            Yelp.at[i,'location__address1'] = each_line.location__address1
    if 'location__address2' and 'location__address3':
        Yelp.drop(columns = ['location__address2','location__address3'],inplace = True)
    return Yelp


### Google attractions have multiple types with one attraction
def merge_types_GoogleAttraction(Google_Attraction):
    if 'results__types__003' and 'results__types__002' in Google_Attraction.columns:
        for i,each_line in Google_Attraction.iterrows():
            if each_line.results__types__003 == each_line.results__types__003:
                each_line.results__types__001 = each_line.results__types__001 + ', ' + each_line.results__types__002 + ', ' + each_line.results__types__003
            elif each_line.results__types__002 == each_line.results__types__002:
                each_line.results__types__001 = each_line.results__types__001 + ', ' + each_line.results__types__002
            Google_Attraction.at[i,'results__types__001'] = each_line['results__types__001']
        if 'results__types__003' and 'results__types__002' in Google_Attraction.columns:
            Google_Attraction.drop(columns=['results__types__003','results__types__002'],inplace = True)
    return Google_Attraction



### We have many google attractions data, so this is for automatically open data file one by one
def collect_GoogleAttraction():
    files = [
            'AmusementPark','Aquarium','ArtGallery',
            'Casino','Museum','Park',
            'ShoppingMall','thingsToDoInNewYork','Zoo'
            ]
    colDropGoogleAttraction = [
            'results__geometry__viewport__|',
            'results__geometry__viewport__|__lat',
            'results__geometry__viewport__|__lng',
            'results__opening_hours__open_now',
            ]
    Google_dict = {}
    for file in files:
        if file not in Google_dict.keys():
            Google_dict[str('Google_Attraction_'+ file)] = pd.read_csv('./Google_Attraction_List/'+ file + '.csv').dropna(subset=['results__formatted_address']).drop(columns = colDropGoogleAttraction,axis=1)
    return Google_dict

# Just Get the Yelp Data, and eliminate some columns
colDropYelp = [
    'transactions__001',
    'transactions__002',
    'transactions__003',
    'location__display_address__003',
    'location__display_address__002',
    'location__display_address__001'
]
Yelp = pd.read_csv('./Yelp_Data/outputfile.csv').dropna(subset=['id']).drop(columns = colDropYelp,axis=1)

if __name__ == '__main__':
    merge_location_Yelp(Yelp).to_csv('./Data_Cleaned/Yelp_Clean.csv')
    collect_GoogleAttraction()
    for item in Google_dict.keys():
        merge_types_GoogleAttraction(Google_dict[item]).to_csv('./Data_Cleaned/'+ item +'.csv')
