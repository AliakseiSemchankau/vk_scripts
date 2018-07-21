from pprint import pprint
import time
from functools import lru_cache
import pickle 

#same as get_community_size, but used to process several communities
def get_community_sizes(id_list, api, access_token, version):
    result = api.groups.getById(
        group_ids=','.join([str(id) for id in id_list]),
        access_token=access_token,
        v=version,
        fields=['members_count'])
    for item in result:
        yield item['id'], item['members_count']

def get_community_size(community_id, api, access_token, version):
    while True:
        time.sleep(0.4)
        try:
            return api.groups.getMembers(
                    group_id=community_id,
                    offset=0,
                    count=0,
                    access_token=access_token,
                    v=version)['count']
        except Exception as e:
            print(e)

def get_ids(community_id, api, access_token, version, limit=-1):
    count = get_community_size(community_id, api, access_token, version)
    if limit > 0:
        count = limit
    member_reading_limit = 1000
    current_offset = 0
    ids = []
    while current_offset < count:
        try:
            members = api.groups.getMembers(
                    group_id=community_id,
                    offset=current_offset,
                    count=member_reading_limit,
                    access_token=access_token,
                    v=version
            )
            ids += members['items']
            current_offset += member_reading_limit
            time.sleep(0.2)
        except Exception as e:
            pass
    return count, ids

def get_communities(user_id, threshold, api, access_token, version):
    while True:
        try:
            time.sleep(0.4)
            communities = api.users.getSubscriptions(
                    user_id=user_id,
                    offset=0,
                    count=threshold,
                    access_token=access_token,
                    v=version,
                    fields=['id', 'name'],
                    extended=True
                )
            subscrs = []
            for item in communities['items']:
                subscrs.append((item['id'], item['name']))

            return subscrs
        except Exception as e:
            print('le exception: {}'.format(e))
            return []

class DataBase():

    def __init__(self):
        self.cache_communities = {}
        self.cache_community_size = {}
        self.cache_ids = {}

class DataBaseOperator():

    def __init__(self, api, access_token, version):
        self.api = api
        self.access_token = access_token
        self.version = version
        self.db = DataBase()

    def load(self, filename):
        try:
            self.db = pickle.load(open(filename, 'rb'))
        except Exception as e:
            print(e)
            self.db = DataBase()

    def dump(self, filename):
        pickle.dump(self.db, open(filename, 'wb'))

    def get_community_size(self, community_id):
        if community_id not in self.db.cache_community_size:
            self.db.cache_community_size[community_id] = \
                get_community_size(community_id,
                                   self.api,
                                   self.access_token,
                                   self.version)
        return self.db.cache_community_size[community_id]

    def get_ids(self, community_id):
        if community_id not in self.db.cache_ids:
            self.db.cache_ids[community_id] = \
                get_ids(community_id,
                        self.api,
                        self.access_token,
                        self.version)
        return self.db.cache_ids[community_id]
    
    def get_communities(self, user_id, threshold):
        if user_id not in self.db.cache_communities:
            self.db.cache_communities[user_id] = \
                get_communities(user_id,
                                200,
                                self.api,
                                self.access_token,
                                self.version)
        return self.db.cache_communities[user_id][:threshold]