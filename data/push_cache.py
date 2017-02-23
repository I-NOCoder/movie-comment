# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '..')

from app import create_app
from models import Movie, search, suggest

create_app()

movie_names = [movie.name for movie in Movie.objects.all()]

text_set = set()

for name in movie_names:
    for w in [name[:i] for i in range(1, len(name) + 1)]:
        text_set.add(w)

# suggest预热
for text in text_set:
    #print 'cache suggest', text
    suggest(text)

# search预热
for movie in Movie.objects.all():
    print 'cache search movie', movie.id
    search(movie.id, 'movie')

