import pickle
import collections
import operator

def load_msg_list(file_name):
    return pickle.load(open(file_name, 'rb'))

with open('parameters.txt', 'r') as parameters:
    TOKEN = parameters.readline().split(' ')[0]
    peer_id = int(parameters.readline().split(' ')[0])
    file_photo_info_name = parameters.readline().split(' ')[0]
    file_likes_stat_name = parameters.readline().split(' ')[0]

print(TOKEN)
print(peer_id)
print(file_photo_info_name)
print(file_likes_stat_name)

attach_msgs = load_msg_list(file_likes_stat_name)

print(attach_msgs[0])

print(len(attach_msgs))

cleared_msgs = []

for msg in attach_msgs:
    if msg['owner_id'] > 0:
        cleared_msgs.append(msg)
attach_msgs = cleared_msgs

print (len(attach_msgs))


class Photo:

    def __init__(self, msg):
        self.owner_id = msg['owner_id']
        self.likes = msg['likes']['count']
        self.likers = msg['likes']['users']
        sizes = ['src_xbig', 'src_big', 'src', 'src_small']
        for src in sizes:
            if src in msg:
                self.src = msg[src]
                break

    def __str__(self):
            return 'vk.com/id{}\nколичество лайков: {}\n{}\n\n'.format(self.owner_id, self.likes, self.src)
            # return 'id:{}, likes:{}, src:{}, likers:{}'.format(self.owner_id, self.likes, self.src, self.likers)


class User:

    def __init__(self, id):
        self.id = id
        self.liked = collections.defaultdict(int)
        self.likers = collections.defaultdict(int)
        self.pictures = 0
        self.likes = 0
        self.likes_given = 0

    def __str__(self):
        return '''vk.com/id{}, likes={}, pictures={}, like_conversion={}\n'''.format(self.id, self.likes, self.pictures, self.likes / self.pictures)
        # return '''vk.com/id{}, likes given : {}'''.format(self.id, self.likes_given)

    def print(self):
        print('vk.com/id' + str(self.id))
        print('pictures=' + str(self.pictures))
        print('likes=' + str(self.likes))
        print('likes_given=' + str(self.likes_given))
        print('кого лайкал:')
        for key, value in sorted(self.liked.items(), key=operator.itemgetter(1), reverse=True):
            print ('vk.com/id' + str(key) +
                   ", лайки:" + str(value) +
                   ", нормировочный коэффициент: " + str((value + 0.) / users[key].pictures))
            if key == self.id:
                print ('внимание, самолайк!')
        print('кто лайкал:')
        for key, value in sorted(self.likers.items(), key=operator.itemgetter(1), reverse=True):
            print ('vk.com/id' + str(key) + ", лайки: " + str(value))
        print('\n\n\n')

photos = [Photo(msg) for msg in attach_msgs if 'likes' in msg]

# print (len(photos))

sorted_photos = sorted(photos, key=lambda photo : photo.likes, reverse=True)

for photo in sorted_photos[:100]:
    print(photo)

ids = set([photo.owner_id for photo in photos])
# print(ids)

users = {id : User(id) for id in ids}

for photo in sorted_photos:
    users[photo.owner_id].likes += photo.likes
    users[photo.owner_id].pictures += 1
    for liker in photo.likers:
        users[photo.owner_id].likers[liker] += 1
        if liker in ids:
            users[liker].liked[photo.owner_id] += 1
            users[liker].likes_given += 1

for user in sorted(users.values(), key = lambda user : user.pictures, reverse=True):
    user.print()






