import vk
import pickle
import time
from pprint import pprint
from parameters import access_token, version, database_address
from community_loader import *
from statistics import quality, get_proba, points, trivial_points, relation
from collections import Counter
from random import shuffle

session = vk.Session()
api = vk.API(session)

community_id = 87998095

dbo = DataBaseOperator(api, access_token, version)
dbo.load(database_address)
N, ids = dbo.get_ids(community_id)
print('N = {}'.format(N))

shuffle(ids)

communities = Counter()

for i, id in enumerate(ids):
    if i % 100 == 0:
        print(i)
        # dbo.dump(database_address)
    subscrs = dbo.get_communities(id, 40)
    for i, community in enumerate(subscrs):
        communities[community] += 1
    
   

popular_communities = communities.most_common(500)

community_sizes = {}
community_ids = [item[0][0] for item in popular_communities]
for id, size in get_community_sizes(community_ids, api, access_token, version):
    community_sizes[id] = size

print('dirty sorting')
popular_communities.sort(key = lambda x: relation(x[1], community_sizes[x[0][0]]), reverse=True)
# pprint(popular_communities)
for item in popular_communities[:100]:
    print('https://vk.com/wall-{}, {}, #: {}, #: {}, %: {}'.format(
        item[0][0],
        item[0][1],
        item[1], 
        community_sizes[item[0][0]],
        100 * relation(item[1], community_sizes[item[0][0]])))

dbo.dump(database_address)