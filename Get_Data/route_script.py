import os
import json
import requests
import pandas
from API_KEY import API_KEY

df = pandas.read_csv('./assemblyData.csv')
resdf = pandas.DataFrame(columns = ['From','Forn_name','To','To_name','Distance','Distance_val','duration','duration_val','status'])
tot_index = 1
for orig_index, orig in df.iterrows():
	for dest_index, dest in df.iterrows():
		if orig['place_id'] != dest['place_id']:
			print(tot_index)
			if tot_index > 48675:
				print(orig['place_id'] +' to ' + dest['place_id'])
				url = 'https://maps.googleapis.com/maps/api/directions/json'
				params = dict(
				origin='place_id:'+ orig['place_id'],
				destination='place_id:'+ dest['place_id'],
				key=API_KEY )
				r = requests.get(url=url, params = params)
				resjson = r.json()
				if resjson['status'] == 'OK':
					resdf.loc[tot_index]=([orig['place_id'],
						orig['name'],
						dest['place_id'],
						dest['name'],
						resjson['routes'][0]['legs'][0]['distance']['text'],
						resjson['routes'][0]['legs'][0]['distance']['value'],
						resjson['routes'][0]['legs'][0]['duration']['text'],
						resjson['routes'][0]['legs'][0]['duration']['value'],
						resjson['status']])
				else:
					resdf.loc[tot_index]=([orig['place_id'],
						orig['name'],
						dest['place_id'],
						dest['name'],
						'x',
						'x',
						'x',
						'x',
						resjson['status']])

			tot_index += 1
			print resdf	
			if tot_index > 100000:
				break
	resdf.to_csv('dist.csv', sep=',', encoding='utf-8')
	print('writing CSV')


	if tot_index > 100000:
				break
			




# for filename in os.listdir('./list'):
# 	print("================"+ filename)
# 	with open('./list/' + filename) as atr_list:
# 		atr_dict = json.load(atr_list)
# 	total_res = []
# 	for item in atr_dict['results']:
# 		index += 1
# 		print item['name'] 
# 		url = 'https://maps.googleapis.com/maps/api/place/details/json'
# 		params = dict(
# 			place_id=item['place_id'],
# 			fields='name,rating,formatted_phone_number,opening_hours,geometry,formatted_address,place_id,type',
# 			key='AIzaSyAqtxV7VAGQkyqB62dK3fGeiLFH8x70BVk' )

# 		r = requests.get(url=url, params = params)
# 		#print r.json()['result']
# 		total_res.append(r.json()['result'])
		
	
# 	with open('./result/'+filename,'w+') as fout:
# 		json.dump(total_res,fout)
# print 'total item' + str(index)

	