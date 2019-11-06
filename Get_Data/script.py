import os
import json
import requests
from API_KEY import API_KEY

index = 0

for filename in os.listdir('./list'):
	print("================"+ filename)
	with open('./list/' + filename) as atr_list:
		atr_dict = json.load(atr_list)
	total_res = []
	for item in atr_dict['results']:
		index += 1
		print item['name'] 
		url = 'https://maps.googleapis.com/maps/api/place/details/json'
		params = dict(
			place_id=item['place_id'],
			fields='name,rating,formatted_phone_number,opening_hours,geometry,formatted_address,place_id,type',
			key= API_KEY)

		r = requests.get(url=url, params = params)
		#print r.json()['result']
		total_res.append(r.json()['result'])
		
	
	with open('./result/'+filename,'w+') as fout:
		json.dump(total_res,fout)
print 'total item' + str(index)

	