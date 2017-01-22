import pickle

class Photo:

    def __init__(self, post):
        self.likes = post['likes']['count']
        self.day = post['date'] / 86400
        self.second = post['date'] % 86400
        self.wall_link = 'https://vk.com/wall{}?own=1&w=wall{}_{}'.format(post['from_id'],
                                                                          post['from_id'],
                                                                          post['id'])
        attachment = post['attachment']
        photo = attachment['photo']
        sizes = ['src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big', 'src', 'src_small']
        for size in sizes:
            if size in photo:
                self.link = photo[size]
                break

    def __str__(self):
        return 'likes={}'.format(self.likes) + \
               '\nday={}'.format(self.day) + \
               '\nsecond={}'.format(self.second) + \
               '\nlink={}'.format(self.link) + \
               '\nwall_link={}'.format(self.wall_link)

