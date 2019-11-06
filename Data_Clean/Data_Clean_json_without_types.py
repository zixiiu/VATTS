
# coding: utf-8



import pandas as pd
import json


# ## Merge Yelp location
# Yelp location could be messed up because some of the restaurants have extra information about location



def merge_location_Yelp(Yelp):
    for i,each_line in Yelp.iterrows():
        if each_line.location__address2 == each_line.location__address2:
            each_line.location__address1 = str(each_line.location__address1) + ', ' + str(each_line.location__address2) + ', ' + str(each_line.location__city) + ', ' + str(each_line.location__state) + ' ' + str(int(each_line.location__zip_code)) + ', ' + str(each_line.location__country)
            Yelp.at[i,'location__address1'] = each_line.location__address1
        if each_line.location__address3 == each_line.location__address3:
            each_line.location__address1 = str(each_line.location__address1) + ', ' + str(each_line.location__address2) + ', ' + str(each_line.location__city) + ', ' + str(each_line.location__state) + ' ' + str(int(each_line.location__zip_code)) + ', ' + str(each_line.location__country)
            Yelp.at[i,'location__address1'] = each_line.location__address1
#         if (each_line.hours__open__start == each_line.hours__open__start) and (each_line.hours__open__end == each_line.hours__open__end):
#             each_line.hours__open__start = str(int(each_line.hours__open__start)) + '-' + str(int(each_line.hours__open__end))
#             Yelp.at[i,'hours__open__start'] = str(each_line.hours__open__start)
    if 'location__address2' and 'location__address3':
        Yelp.drop(columns = ['location__address2','location__address3'],inplace = True)
    return Yelp



# ## Merge Google_Attraction type
# Google attractions have multiple types with one attraction



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


# ## Open every Google_Attraction
# We have many google attractions data, so this is for automatically open data file one by one



def collect_GoogleAttraction():
    files = [
            'AmusementPark','Aquarium','ArtGallery',
            'Casino','Museum','Park',
            'ShoppingMall','thingsToDoInNewYork','Zoo'
            ]
    Google_dict = {}
    for file in files:
        if file not in Google_dict.keys():
            Google_dict[str('Google_Attraction_'+ file)] = pd.read_json('./Google_Attraction_Detail/'+ file + '.json')
    return Google_dict




def f_Google_dict (Google_dict):
    formatted_Google_dict = {}
    for file in Google_dict.keys():
        if file not in formatted_Google_dict.keys():
            file_name = str('formatted_' + file)
            formatted_Google_dict[file_name] = pd.DataFrame()
            for item in Google_dict[file].keys():
                if item != 'geometry' and item != 'opening_hours':
                    formatted_Google_dict[file_name][item] = Google_dict[file][item].values
                elif item == 'geometry':
                    geometry = Google_dict[file][item].values
                    lat = []
                    lng = []
                    for coord in geometry:
                        lat.append(coord['location']['lat'])
                        lng.append(coord['location']['lng'])
                    formatted_Google_dict[file_name]['lat'] = lat
                    formatted_Google_dict[file_name]['lng'] = lng
#                 elif item == 'opening_hours':
#                     opening_hours = Google_dict[file][item]
#                     for time_item in opening_hours:
#                         for each_day in time_item['periods']:
#                             if type(each_day) != 'float':
#                                 for open_close in each_day:
#                                     operation_hours = ''
#                                     operation_hours = 'day' + str(each_day[open_close]['day']) + '_' + open_close
#                                     formatted_Google_dict[file_name][openning_hours] = each_day[open_close]['time']

    return formatted_Google_dict


# ## Reformat Google_Attraction

# ## Reformat Yelp
# Yelp:
#
# id, name, location__address1+location__city+location__state+location__zip_code+location__country, coordinates__latitude, coordinates__longitude, hours__open__start + hours__open__end, rating, categories__title
#
# attraction__id,attraction__name, attraction__formatted__address, attraction__location__lat, attraction__location__lng, attraction__opening__hours, attraction__rating, results__type



def f_Yelp (Yelp):
    col_f_Yelp = [
        'attraction__id','attraction__name', 'attraction__formatted__address',
        'attraction__location__lat', 'attraction__location__lng', 'attraction__opening__hours',
        'attraction__rating', 'results__type'
    ]
    col_o_Yelp = [
        'id','name',' location__address1',
        'coordinates__latitude','coordinates__longitude',
        'hours__open__start','rating','categories__title'
    ]
    formatted_Yelp = pd.DataFrame()
    n = 0
    for col_name in col_o_Yelp:
        if col_name in Yelp.columns:
            formatted_Yelp[col_f_Yelp[n]] = Yelp[col_name].values
        n += 1
    return formatted_Yelp



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
    merge_location_Yelp(Yelp)
    f_Yelp(Yelp).to_csv('./Data_Cleaned/formatted_Yelp.csv')
    Google_dict = collect_GoogleAttraction()
#     for item in Google_dict.keys():
#         merge_types_GoogleAttraction(Google_dict[item])
    formatted_Google_dict = f_Google_dict(Google_dict)
    for item in formatted_Google_dict.keys():
        formatted_Google_dict[item].to_csv('./Data_Cleaned/'+item+'.csv')


# ## Next thing is to get the data into frame according to our requirement
# Google attraction time from json
#
# Monday: 10:00 AM – 5:00 PM
# Tuesday: 10:00 AM – 5:00 PM
# Wednesday: 10:00 AM – 5:00 PM
# Thursday: 10:00 AM – 5:00 PM
# Friday: 10:00 AM – 5:00 PM
# Saturday: 10:00 AM – 5:30 PM
# Sunday: 10:00 AM – 5:30 PM
#
# day0_close,day0_open
#
# Yelp time from csv
#
# column from Monday to Friday
