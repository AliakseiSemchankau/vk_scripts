This script allows you to get the best photos from any vk.com community.
The quality of post in community is measured by local relation of likes
(not global count of likes, cause it depends on number of followers, which is changing).
More mathematically, it is supposed in this model that count of likes on post
is equal to [quality of post] * [number of followers] * [actual time of day].
So, all at all this heuristic are all about solving this equation.

In parameters.txt you should specify the community_id and count of (new) posts you
want to analyze.

Alternatively, you can just run
' python3 post_analyzer.py --destination=very_best_of_pic_squad -n 8600 --top 30 --id 105800661'
that would read 8600 posts from community with id 105800661 and would save top-30 pictures in folder
very_best_of_pic_squad. Be aware that such folder exist! Each picture is saved with a name 'rang(measure)'.
It's supposed, that if measure is greater than 1, than picture is better than average, and worse vice versa.