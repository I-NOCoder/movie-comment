
from spider.parse_movie import get_movie_info, unprocess_movie


movie_ids = []
try:
    f = open('top250_id.txt', 'r')
except:
    print 'open file error!'
	
for i in f.readlines():
    movie_ids.append(i.strip())

for movie_id in unprocess_movie():
    get_movie_info(movie_id)

for movie_id in movie_ids:
    get_movie_info(movie_id)
