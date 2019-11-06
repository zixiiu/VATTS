from datetime import datetime
from datetime import timedelta
import json



def createtimetable(result):
	start_time = result['start_time'].replace('start','')
	end_time = result['end_time'].replace('end','')
	start_time_obj = datetime.strptime(start_time,'%I%p')
	end_time_obj = datetime.strptime(end_time, '%I%p')

	visit_time = (((end_time_obj-start_time_obj) - timedelta(seconds = sum(result['travel_time'])))/len(result['places']))


	time_table_list = []
	len_place = len(result['places'])
	time_now = start_time_obj
	index = 1
	for item in result['places']:
		#place
		place_start_time = time_now.strftime('%H:%M:%S')
		time_now = time_now + visit_time
		place_end_time = time_now.strftime('%H:%M:%S')
		time_table_list.append({'cat':'place','name': item['name'],'address':item['formatted_address'],'rating':item['rating'],'types':item['types'],'start_time':place_start_time,'end_time':place_end_time,'index':index})

		#transit
		if index < len_place:
			transit_start_time = time_now.strftime('%H:%M:%S')
			time_now = time_now + timedelta(seconds=result['travel_time'][index-1])
			transit_end_time = time_now.strftime('%H:%M:%S')
			time_table_list.append({'cat':'transit','start_time':transit_start_time,'end_time':transit_end_time,'index_from':index,'index_to':index+1, 'duration_sec': result['travel_time'][index-1]})
		index += 1

	time_table_json = json.dumps(time_table_list)
	return time_table_json



if __name__ == '__main__':

	result = {'places': [{'Unnamed: 0': 9, 'name': 'Sean Kelly', 'formatted_address': '475 10th Ave, New York, NY 10018, USA', 'rating': 4.7, 'types': 'art_gallery, point_of_interest, establishment', 'lat': 40.7560796, 'lng': -73.9982615, 'id': 'eba3c1484e314612781eae06254065e014385b6d', 'place_id': 'ChIJWTV4jrZZwokRFYejsehrXyY'}, {'Unnamed: 0': 8, 'name': 'Whitney Museum of American Art', 'formatted_address': '99 Gansevoort St, New York, NY 10014, USA', 'rating': 4.5, 'types': 'museum, point_of_interest, establishment', 'lat': 40.7395877, 'lng': -74.0088629, 'id': '6a6e35a1c9265a5f2b68cb954ba2c06c8dc19093', 'place_id': 'ChIJN3MJ6pRYwokRiXg91flSP8Y'}, {'Unnamed: 0': 13, 'name': 'Pier 51 at Hudson River Park', 'formatted_address': 'Hudson River Greenway, New York, NY 10014, USA', 'rating': 4.6, 'types': 'park, point_of_interest, establishment', 'lat': 40.7382067, 'lng': -74.0107047, 'id': '2b627fef9d8b18e1fb811c02fdcb117cbf3e4261', 'place_id': 'ChIJNUwaa-pZwokRh_DHYDHBWkc'}, {'Unnamed: 0': 37, 'name': 'The High Line', 'formatted_address': 'New York, NY 10011, USA', 'rating': 4.7, 'types': 'park, point_of_interest, establishment', 'lat': 40.7479925, 'lng': -74.0047649, 'id': '72dc79d023feec77725d7336e7c46fee27805319', 'place_id': 'ChIJ5bQPhMdZwokRkTwKhVxhP1g'}, {'Unnamed: 0': 40, 'name': 'Brookfield Place', 'formatted_address': '230 Vesey St, New York, NY 10281, USA', 'rating': 4.5, 'types': 'shopping_mall, point_of_interest, establishment', 'lat': 40.7127168, 'lng': -74.0152824, 'id': '30005ece85c57803e290712f5f70ffc105849cb9', 'place_id': 'ChIJy8jTDBtawokRB9wNyxemSw8'}, {'Unnamed: 0': 9, 'name': "Gulliver's Gate", 'formatted_address': '216 W 44th St, New York, NY 10036, USA', 'rating': 4.6, 'types': 'museum, point_of_interest, establishment', 'lat': 40.757584, 'lng': -73.986995, 'id': '22c5ab41a505113233d98ef454e1a9a91100f713', 'place_id': 'ChIJB3jt8VRYwokR3usmhiCep0o'}], 'travel_time': [701, 405, 114, 140, 419], 'start': {'lat': 40.7149114, 'long': -74.01546119999999}, 'end': {'lat': 40.759011, 'long': -73.9844722}, 'start_time': 'start6am', 'end_time': 'end2pm'}
	createtimetable(result)