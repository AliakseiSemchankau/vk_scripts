import vk
import pickle
import time
from pprint import pprint

session = vk.Session()
api = vk.API(session)

with open('parameters.txt', 'r') as parameters:
    community_id = int(parameters.readline().split(' ')[0])
    count = int(parameters.readline().split(' ')[0])
    file_posts_info = parameters.readline().split(' ')[0]

print('community_id={}'.format(community_id))
print('read posts: {}'.format(count))

current_offset = 0

posts = []

while current_offset < count:
    while True:
        try:
            # print('current_offset={}'.format(current_offset))
            wall = api.wall.get(
                owner_id=community_id,
                offset=current_offset,
                count=100,
                filter='owner'
            )

            for item in wall:
                if isinstance(item, dict):
                    posts.append(item)

            current_offset += 100
            break
            time.sleep(0.2)
        except:
            print('exception:(')
            pass

print('posts={}'.format(len(posts)))
# pprint(posts[-10:])

pickle.dump(posts, open('{}-posts.txt'.format(community_id), 'wb'))
