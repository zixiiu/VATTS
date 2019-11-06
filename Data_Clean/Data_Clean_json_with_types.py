
# coding: utf-8



import pandas as pd
import json


# ## Open every Google_Attraction
# This is from Wenli Zou's data



def collect_Google_Attraction_from_list():
    files = [
            'AmusementPark','Aquarium','ArtGallery',
            'Casino','Museum','Park',
            'ShoppingMall','thingsToDoInNewYork','Zoo'
            ]
    Google_dict = {}
    for file in files:
        if file not in Google_dict.keys():
            with open('./Google_Attraction_List/' + file + '.json') as json_data:
                Google_dict[str('Google_Attraction_'+ file)] = json.load(json_data)
    return Google_dict


# ## Reformat Google_Attraction



def f_Google_list (Google_dict):
    formatted_Google_dict = {}
    for file in Google_dict.keys():
        if file not in formatted_Google_dict.keys():
            file_name = str('formatted_' + file)
            formatted_Google_dict[file_name] = pd.DataFrame()
            name = []
            formatted_address = []
            id_a = []
            place_id = []
            rating = []
            types = []
            lat = []
            lng = []
            for one_level in Google_dict[file]['results']:
                for two_level in one_level.keys():
                    if two_level == 'id':
                        id_a.append(one_level[two_level])
                    if two_level == 'place_id':
                        place_id.append(one_level[two_level])
                    if two_level == 'name':
                        name.append(one_level[two_level])
                    if two_level == 'formatted_address':
                        formatted_address.append(one_level[two_level])
                    if two_level == 'rating':
                        rating.append(one_level[two_level])
                    if two_level == 'types':
                        myString = ", ".join(map(str, one_level[two_level]))
                        types.append(myString)
                    if two_level == 'geometry':
                        geometry = one_level[two_level]
                        lat.append(geometry['location']['lat'])
                        lng.append(geometry['location']['lng'])
            formatted_Google_dict[file_name]['name'] = name
            formatted_Google_dict[file_name]['formatted_address'] = formatted_address
            formatted_Google_dict[file_name]['rating'] = rating
            formatted_Google_dict[file_name]['types'] = types
            formatted_Google_dict[file_name]['lat'] = lat
            formatted_Google_dict[file_name]['lng'] = lng
            formatted_Google_dict[file_name]['id'] = id_a
            formatted_Google_dict[file_name]['place_id'] = place_id
    return formatted_Google_dict


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
    Google_dict = collect_Google_Attraction_from_list()
#     for item in Google_dict.keys():
#         merge_types_GoogleAttraction(Google_dict[item])
    formatted_Google_dict = f_Google_list(Google_dict)
    for item in formatted_Google_dict.keys():
        formatted_Google_dict[item].to_csv('./Data_Cleaned/'+item+'.csv')
