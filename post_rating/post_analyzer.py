from skimage import io
import pickle
from photo import Photo
from collections import defaultdict
from pprint import pprint
import math
import os
import argparse

QUANTILE = 0.1
SECS = 7200
SEQUENCE = 50

def get_photos(file_name):
    return pickle.load(open(file_name, 'rb'))

def get_photo_rates(photos, expectations):
    exp_rates = [photo.likes / expectations[photo.second // SECS] for photo in photos]
    soft_avgs = [soft_avg(exp_rates[t:t+SEQUENCE]) for t in range(len(exp_rates)-SEQUENCE)]
    return [[photo, math.log(exp_rate / avg + 1) / math.log(2.0)]
            for photo, avg, exp_rate in
            zip(photos, soft_avgs, exp_rates)]

def soft_avg(likes):
    left_quantile = int(QUANTILE * len(likes))
    right_quantile = int((1 - QUANTILE) * len(likes))
    sorted_likes = sorted(likes)
    sorted_likes = sorted_likes[left_quantile:right_quantile]
    return sum(sorted_likes)/(len(sorted_likes) + 0.0)

def main():
    parser = argparse.ArgumentParser(description="parsing communities with picture content",)

    parser.add_argument("--destination", "-d", type=str, help="folder for storing loaded pictures")
    parser.add_argument("--id", type=int, help="community id")
    parser.add_argument("--count", "-n", type=int, help="number of (new) posts to load")
    parser.add_argument("--top", type=int, help="count of pictures to be saved in folder")

    args = parser.parse_args()
    print(args)

    destination = args.destination
    community_id = args.id
    top = args.top

    with open('parameters.txt', 'w') as parameters:
        parameters.write('-{} # community id\n'.format(community_id))
        parameters.write('{} # count\n'.format(args.count))

    exec(open('./posts_loader.py').read())
    exec(open('./post_processor.py').read())

    photos = get_photos('{}-photos.txt'.format(-community_id))[::-1]
    photos = [photo for photo in photos if photo.likes]
    print('count of photos={}'.format(len(photos)))

    photos_div_t = defaultdict(list)
    for photo in photos:
        photos_div_t[photo.second // SECS].append(photo)

    avgs = [sum([photo.likes for photo in sub_photos]) / len(sub_photos) for sub_photos in photos_div_t.values()]
    norm_avgs = [len(avgs) * avg / sum(avgs) for avg in avgs]

    photo_rates = get_photo_rates(photos, norm_avgs)
    photo_rates.sort(key=lambda p_r: p_r[1], reverse=True)
    for index, p_r in enumerate(photo_rates[0:top]):
        img = io.imread(p_r[0].link)
        io.imsave('{}/{}({}).png'.format(destination, index, p_r[1]), img)

if __name__ == '__main__':
    main()