This script allows you to get the best photos from any vk.com community.
The quality of post in community is measured by local relation of likes
(not global count of likes, cause it depends on number of followers, which is changing).
More mathematically, it is supposed in this model that count of likes on post
is equal to [quality of post] * [number of followers] * [actual time of day].
So, all at all this heuristic are all about solving this equation.

In parameters.txt you should specify the community_id and count of (new) posts you
want to analyze.