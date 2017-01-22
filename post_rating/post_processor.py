import vk
import pickle
import time
from pprint import pprint
from photo import Photo


session = vk.Session()
api = vk.API(session)

def get_posts(file_name):
    return pickle.load(open(file_name, 'rb'))

with open('parameters.txt', 'r') as parameters:
    community_id = int(parameters.readline().split(' ')[0])
    count = int(parameters.readline().split(' ')[0])
    file_posts_info = parameters.readline().split(' ')[0]

# print(community_id)
# print(count)

current_offset = 0

posts = get_posts('{}-posts.txt'.format(community_id))
# print(len(posts))
photos = []

for post in posts:
    if 'attachment' in post and \
                    'photo' in post['attachment'] and \
                    'attachments' in post and \
                    len(post['attachments']) == 1:
            photos.append(Photo(post))

print('photos: {}'.format(len(photos)))
# for photo in photos:
#     print(photo)
pickle.dump(photos, open('{}-photos.txt'.format(community_id), 'wb'))