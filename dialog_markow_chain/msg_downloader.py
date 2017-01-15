import vk
import pickle
import time
session = vk.Session()
api = vk.API(session)

with open('parameters.txt', 'r') as parameters:
    TOKEN = parameters.readline().split(' ')[0]
    chat_id = int(parameters.readline().split(' ')[0])
    file_downloaded_msgs_name = parameters.readline().split(' ')[0]
    length = int(parameters.readline().split(' ')[0])
    predicts = parameters.readline().split(' ')[:3]
    ids = set([int(id) for id in parameters.readline().split('#')[0].split(' ') if len(id) > 0])

print(TOKEN)
print(chat_id)
print(file_downloaded_msgs_name)
print(length)
print(predicts)
print(ids)

flag = True
offset = 0
msg_list = []
while flag:
    print('offset={}'.format(offset))
    time.sleep(0.5)
    history = api.messages.getHistory(
        user_id=chat_id,
        access_token=TOKEN,
        rev=1,
        count=200,
        offset=offset)

    for obj in history:
        if isinstance(obj, dict):
            msg_list.append(obj)

    offset += 200
    if len(history) < 5:
        flag = False

pickle.dump(msg_list, open(file_downloaded_msgs_name, 'wb'))

