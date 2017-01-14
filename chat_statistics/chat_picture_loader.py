import vk
import pickle
import time

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

attach_msgs = []

flag = True
start_from = None
iteration = 0
while flag:
    print('start_from=' + str(start_from))
    iteration += 1
    print ('iteration=' + str(iteration))
    time.sleep(0.3)
    response = api.messages.getHistoryAttachments(
        media_type='photo',
        start_from=start_from,
        peer_id=peer_id,
        count=200,
        access_token=TOKEN)

    if 'next_from' in response:
        start_from = response['next_from']
        response.pop('next_from', None)
    else:
        pickle.dump(response, open('log.txt', 'wb'))
        print (response)
        break

    if len(response.keys()) < 5:
        break

    for key in response.keys():
        item = response[key]
        if isinstance(item, dict) and 'photo' in item.keys():
            attach_msgs.append(item['photo'])

pickle.dump(attach_msgs, open(file_photo_info_name, 'wb'))