from Graph import Graph
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist



def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = int(graph.weights[(current_node, next_node)]) + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path


graph = Graph()
# each node should be represented by the id of the position

# initially all weights of the edges should represent the distance between two attractions
# for the algorithm to function optimally, we need to make sure that only attractions
# that are at least X distance away from each other has an edge
# *****************need to tweak X after have the data!***********

# Then we need to adjust weight base on user's preference and stay time
# (minus a value to weight when the point is in user preferred category)
# (add a value to weight weight base on visit category)

# edges = [
#     ('X', 'A', 7),
#     ('X', 'B', 2),
#     ('X', 'C', 3),
#     ('X', 'E', 4),
#     ('A', 'B', 3),
#     ('A', 'D', 4),
#     ('B', 'D', 4),
#     ('B', 'H', 5),
#     ('C', 'L', 2),
#     ('D', 'F', 1),
#     ('F', 'H', 3),
#     ('G', 'H', 2),
#     ('G', 'Y', 2),
#     ('I', 'J', 6),
#     ('I', 'K', 4),
#     ('I', 'L', 4),
#     ('J', 'L', 1),
#     ('K', 'Y', 5),
# ]

# only select points that the user is interested in
def findPossiblePoints(interestType):
    pattern = '|'.join(interestType)
    points = pd.read_csv('Datas/assemblyData.csv')

    food = points[points.types.str.contains('food')]
    # start = 'ChIJf2_0qFVYwokRcbTtlS60Vqg'
    # end = 'ChIJy8jTDBtawokRB9wNyxemSw8'
    # startP = points[points['place_id']==start]
    # endP = points[points['place_id'] == end]
    points =points[points.types.str.contains(pattern)]
    # print(food)
    return points, food



def buildGraph(threashold,start, end,points, food):
    distances = pd.read_csv('Datas/Distances.csv')
    distances = distances[distances['duration']!='x']
    distances['duration'] = distances['duration_val']
    # distances['duration'], distances['mins'] = distances['duration'].str.split(' ', 1).str
    distances = distances[['From','To','duration']]
    invalid = distances[(distances['From'] == start) & (distances['To'] == end)]
    distances = distances[(distances['From']!=start) | (distances['To']!=end)]
    distances = distances[(distances['From'] != end) | (distances['To'] != start)]
    # print(points['place_id'])
    # print(distances.shape)
    distances = distances[distances['From'].isin(points['place_id'])]
    distances = distances[distances['To'].isin(points['place_id'])]
    distances['duration'].astype(str).astype(int)
    distanceCopy = distances.copy()
    dis = distances.merge(points, left_on='To', right_on='place_id', how='inner')
    dis = dis[['From','To','duration','rating']]
    dis.duration = pd.to_numeric(dis.duration, errors='coerce').fillna(0).astype(np.int64)
    dis.rating = pd.to_numeric(dis.rating, errors='coerce').fillna(0).astype(np.float)

    dis = dis[dis['duration']<threashold]
    dis['duration'] = dis['duration']
    # dis['weight'] = dis['duration']
    distances = dis[['From','To','duration']]

    # print(distances.head())
    edges = list(zip(*[distances[c].values.tolist() for c in distances]))
    for edge in edges:
        graph.add_edge(*edge)
    return distanceCopy



def checkValidPath(path, distances, duration):
    dis = []
    # print(path)
    for i in range(len(path)-1):
        du = distances[(distances['From']==path[i]) & (distances['To']==path[i+1])].iloc[0]['duration']
        dis.append(int(du))
    print('travel time in seconds are:',dis)
    sum = 0
    for i in dis:
        sum+=i
    sum/=60
    sum+=(len(dis)+1)*60
    print("allowed total time is ", duration)
    print("trip total time is ",sum)
    return sum<duration, dis

def findRestaurant(pathDetailed,food,j):
    food1 = food[['place_id','lat','lng']]
    foodD = food1[food1['place_id']==j]

    path1 = pathDetailed[['place_id','lat','lng']]
    mat =cdist(food1[['lat', 'lng']],
               path1[['lat', 'lng']], metric='euclidean')
    distances = pd.DataFrame(mat, index=food1['place_id'], columns=path1['place_id'])
    distances = distances.sort_values(distances.columns[j], ascending=True)
    foodIds = list(distances.index)[:5]
    foodNearby = food[food['place_id'].isin(foodIds)]
    return foodNearby
    # print(foodNearby)


def findroutemain(start, end, interestedTYPE):
    points, food = findPossiblePoints(interestedTYPE)
    points = points.drop_duplicates(['place_id'], keep='first')
    threashold = 500
    # buildGraph(threashold, start, end,points, food)

    finished = False
    counter = 0


    while((not finished) and counter<20):
        # distances = buildGraph(threashold,start, end)
        distances = buildGraph(threashold, start, end, points, food)

        finished = True
        counter+=1
        print('Try',counter)
        # dijsktra(graph, 'ChIJbcr95-1YwokRuBMO1wMVL50', 'ChIJeQYDhQ5dwokRyqawBQIG_TM')

        path = dijsktra(graph, start, end)

        if path=="Route Not Possible":
            print("No route found")
            print()
            finished = False
            threashold+=300*counter
        else:
            print(path)
            valid, distimelist = checkValidPath(path, distances, 300)
            if not valid:
                print("too many points")
                print(path)
                print()
                finished = False
                threashold += 300 * counter
    def closest_point(point, points):
        """ Find closest point from a list of points. """
        return points[cdist([point], points).argmin()]

    # print(points)
    #print(path)

    pathDetailed = points[points['place_id'].isin(path)]
    # print(pathDetailed)


    for i in path:
        place = points[points['place_id']==i].iloc[0]
        # print(place)
        print('Name:', place['name'])
        print('Address:', place['formatted_address'], '\tRating:', place['rating'], '\tType:', place['types'])

    print()
    print('--------------Food Nearby Info--------------')
    j = 0
    for i in path:
        place = points[points['place_id']==i].iloc[0]
        # print(place)
        print('Name:', place['name'])
        print('Address:', place['formatted_address'], '\tRating:', place['rating'], '\tType:', place['types'])
        # print('id:',i)
        print('Sugested restaurant are:')
        foodNearby = findRestaurant(pathDetailed, food,j)
        for index, row in foodNearby.iterrows():
            print('Name:', row['name'])
            print('Address:', row['formatted_address'], '\tRating:', row['rating'], '\tType:', row['types'])
        j+=1
        print()
    valid, distimelist = checkValidPath(path, distances, 300)
    return pathDetailed.to_json(orient = 'records'),distimelist
# print(path)

if __name__ == '__main__':
    start = 'ChIJdWA_r4tZwokRPgHkRNHAKog'
    # end = 'ChIJBUJLolKRwokRCIrIkXtAmAU'
    # end ='ChIJFxXcxfpYwokR4SxqEQVpaLk'
    # end = 'ChIJwZCT7bdZwokRNx1YURTRbmM'
    end='ChIJh7tBHr7ywokR4hFTwLzlguk'
    # end = 'ChIJNwg-C-dYwokR7pFow7mu9cc'
    #end ='ChIJFxXcxfpYwokR4SxqEQVpaLk'

    # start = 'ChIJf2_0qFVYwokRcbTtlS60Vqg'
    # end = 'ChIJy8jTDBtawokRB9wNyxemSw8'
    interestType = ['museum', 'casino', 'art_gallery']
    json_1,json_2 = findroutemain(start,end,interestType)
    # print(json_1)