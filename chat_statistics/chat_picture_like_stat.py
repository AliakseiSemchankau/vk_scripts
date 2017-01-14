import vk
import pickle
import time

def load_msg_list(file_name):
    return pickle.load(open(file_name, 'rb'))

session = vk.Session()
api = vk.API(session)

with open('parameters.txt', 'r') as parameters:
    TOKEN = parameters.readline().split(' ')[0]
    peer_id = int(parameters.readline().split(' ')[0])
    file_photo_info_name = parameters.readline().split(' ')[0]
    file_likes_stat_name = parameters.readline().split(' ')[0]

print(TOKEN)
print(peer_id)
print(file_photo_info_name)
print(file_likes_stat_name)

attach_msgs = load_msg_list(file_photo_info_name)

print(len(attach_msgs))

iteration = 0

updated_msgs = []

for msg in attach_msgs:
    try:
        time.sleep(0.5)
        msg_likes_list = api.likes.getList(
            type='photo',
            owner_id=msg['owner_id'],
            item_id=msg['pid'],
            access_token=TOKEN,
            access_key=msg['access_key'])
        iteration += 1
        if iteration % 100 == 0:
            print(msg_likes_list)
            print('iteration=' + str(iteration))
        msg['likes'] = msg_likes_list
        updated_msgs.append(msg)
    except:
        print('exception for:')
        print(msg)

pickle.dump(updated_msgs, open(file_likes_stat_name, 'wb'))
