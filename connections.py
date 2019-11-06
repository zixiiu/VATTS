import FindRoute
import json
import requests
import pandas
import API_KEY


def address2latlong(address):
    address = address.replace(' ','+').replace(',','')
    print(address)
    #'https://maps.googleapis.com/maps/api/place/textsearch/json?query=museum+in+newyork&hasNextPage=true&key=AIzaSyDtTUhDargYcn_fgIsBVDMXjkBviCdliYk'
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = dict(
        query=address + '+in+newyork',
        key=API_KEY.API_KEY)

    r = requests.get(url=url, params=params)
    lat = r.json()['results'][0]['geometry']['location']['lat']
    long = r.json()['results'][0]['geometry']['location']['lng']

    return lat,long

def find_closest_POI(inputlat,inputlong,interestTYPE,exempt=None):
    df = pandas.read_csv('./Datas/assemblyData.csv')
    closest = None
    for d_index, d in df.iterrows():
        if d_index == 0:
            closest = d
            closest_dist = abs(d['lat'] - float(inputlat)) + abs(d['lng'] - float(inputlong))
        else:
            dist = abs(d['lat'] - float(inputlat)) + abs(d['lng'] - float(inputlong))
            if dist < closest_dist and not set(d['types'].split(', ')).isdisjoint(interestTYPE) and d['place_id'] != exempt:
                closest = d
                closest_dist = dist

    return closest
    #print(df)



def connection_main(start_address,end_address,interestedTYPE,start_time,end_time):
    start_lat, start_long = address2latlong(start_address)
    end_lat, end_long = address2latlong(end_address)
    startPOI_df = find_closest_POI(start_lat, start_long, interestedTYPE)
    endPOI_df = find_closest_POI(end_lat, end_long, interestedTYPE, startPOI_df['place_id'])
    res_place_json, res_timelist = FindRoute.findroutemain(startPOI_df['place_id'], endPOI_df['place_id'],
                                                           interestedTYPE)
    print(startPOI_df['place_id'])
    print(startPOI_df['name'])
    print(endPOI_df['place_id'])
    print(endPOI_df['name'])

    jsobj = json.loads(res_place_json)
    idlist = [0]
    uniqlist = []
    for items in jsobj:
        if items['place_id'] not in idlist:
            idlist.append(items['place_id'])
            uniqlist.append(items)



    comb_res = {"places": uniqlist, "travel_time":res_timelist, "start": {"lat":start_lat,'long':start_long},'end':{'lat':end_lat,'long':end_long}, "start_time": start_time, "end_time":end_time }
    #print(json.dumps(comb_res))
    return comb_res

if __name__ == '__main__':
    #start = 'ChIJdWA_r4tZwokRPgHkRNHAKog'
    # end = 'ChIJBUJLolKRwokRCIrIkXtAmAU'
    # start ='ChIJFxXcxfpYwokR4SxqEQVpaLk'
    # end = 'ChIJwZCT7bdZwokRNx1YURTRbmM'
    #end='ChIJh7tBHr7ywokR4hFTwLzlguk'
    #end = 'ChIJNwg-C-dYwokR7pFow7mu9cc'
    # end ='ChIJFxXcxfpYwokR4SxqEQVpaLk'

    #print(res_place_json)
    #res_timelist_json = json.dumps(res_timelist)
    #print(res_place_json)

    ####test2
    # start_address = '1568 Broadway, New York, NY 10036'
    # end_address = '1400 Bergen St'
    # #start
    # start_lat, start_long  = address2latlong(start_address)
    # end_lat, end_long = address2latlong(end_address)
    # #res_lat = '40.759917';res_long = '-73.98452979999999'
    # startPOI_df = find_closest_POI(start_lat,start_long,['park'])
    # endPOI_df = find_closest_POI(end_lat, end_long,['park'])
    # print(startPOI_df['place_id'])
    # print(startPOI_df['name'])
    # print(endPOI_df['place_id'])
    # print(endPOI_df['name'])
    #
    # res_place_json, res_timelist = FindRoute.findroutemain(startPOI_df['place_id'], endPOI_df['place_id'],['park','library'])
    # print(res_place_json)

    ####ultimate test
    #start_address = '1568 Broadway, New York, NY 10036'
    #end_address = '1400 Bergen St'
    start_address = 'central park'
    end_address = 'time square'
    res_place_json= connection_main(start_address,end_address,['park','museum','casino'])
    print(res_place_json)