
# coding: utf-8



import pandas as pd


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
    colDropGoogleAttraction = [
            'results__geometry__viewport__|',
            'results__geometry__viewport__|__lat',
            'results__geometry__viewport__|__lng',
            ]
    Google_dict = {}
    for file in files:
        if file not in Google_dict.keys():
            Google_dict[str('Google_Attraction_'+ file)] = pd.read_csv('./Google_Attraction_List/'+ file + '.csv').dropna(subset=['results__formatted_address']).drop(columns = colDropGoogleAttraction,axis=1)
    return Google_dict


# ## Reformat Google_Attraction
# Google_Attraction:
#
# results__id, results__name, results__formatted__address, results__geometry__location__lat, results__geometry__location__lng, results__opening_hours__open_now, results__rating, results__types__001
#
# attraction__id,attraction__name, attraction__formatted__address, attraction__location__lat, attraction__location__lng, attraction__opening__hours, attraction__rating, results__type



def f_Google_dict (Google_dict):
    col_f_Google = [
        'attraction__id','attraction__name', 'attraction__formatted__address',
        'attraction__location__lat', 'attraction__location__lng', 'attraction__opening__hours',
        'attraction__rating', 'results__type'
        ]
    col_o_Google = [
        'results__id', 'results__name', 'results__formatted_address',
        'results__geometry__location__lat', 'results__geometry__location__lng', 'results__opening_hours__open_now',
        'results__rating', 'results__types__001'
        ]
    formatted_Google_dict = {}
    for file in Google_dict.keys():
        n = 0
        if file not in formatted_Google_dict.keys():
            formatted_Google_dict[str('formatted_' + file)] = pd.DataFrame()
            for col_name in col_o_Google:
                if col_name in Google_dict[file].columns:
                    formatted_Google_dict[str('formatted_' + file)][col_f_Google[n]] = Google_dict[file][col_name].values
                else:
                    formatted_Google_dict[str('formatted_' + file)][col_f_Google[n]] = Google_dict[file]['results__types'].values
                n += 1
    return formatted_Google_dict



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
    for item in Google_dict.keys():
        merge_types_GoogleAttraction(Google_dict[item])
    formatted_Google_dict = f_Google_dict(Google_dict)
    for item in formatted_Google_dict.keys():
        formatted_Google_dict[item].to_csv('./Data_Cleaned/'+item+'.csv')


# ## Next thing is to get the data into frame according to our requirement
