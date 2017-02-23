# -*- coding: utf-8 -*-

import ast
from ext import db
from datetime import datetime

from mongoengine.queryset import DoesNotExist
from libs.rdstore import cache

MOVIE_URL = 'https://movie.douban.com/subject/{}/'
COMMENT_URL = 'https://movie.douban.com/subject/{}/comments?status=P'
USER_URL = 'https://www.douban.com/people/{}/'

SAMPLE_SIZE = 50
TOTAL_SIZE = 200

START_KEY = 'commentbox:start'
OBJ_KEY = 'commentbox:object:{coll_name}:{id}'
SEARCH_KEY = 'commentbox:search:{type}:{id}'
SUGGEST_KEY = 'commentbox:suggest:{text}'
TIMEOUT = 60*60


class BaseModel(db.Document):
    id = db.StringField(primary_key=True)
    create_at = db.DateTimeField(default=datetime.now())
    update_at = db.DateTimeField()

    meta = {
        "allow_inheritance": True,
        'abstract': True,
        'strict': False
    }

    @classmethod
    def get(cls, id):
        coll_name = cls._meta['collection']
        key = OBJ_KEY.format(coll_name=coll_name, id=id)
        rs = cache.get(key)
        if rs:
            return cls.from_json(rs)
        rs = cls.objects.get(id=id)
        cache.set(key, rs.to_json())
        return rs

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(i) for i in ids if i]

    @classmethod
    def get_or_create(cls, **kwargs):
        try:
            return cls.objects.get(id=kwargs['id'])
        except DoesNotExist:
            kwargs.update({'update_at': datetime.now()})
            model = cls(**kwargs)
            model.save()
            return model

    @classmethod
    def get_sample_ids(cls, size):
        samples = list(cls.objects.aggregate(
            {'$sample':{'size': size}}
        ))
        return [s['_id'] for s in samples]


class Movie(BaseModel):
    name = db.StringField()
    mark = db.StringField()
    picture = db.StringField()

    meta = {
        'indexes': ['name']
    }

    @property
    def url(self):
        return MOVIE_URL.format(self.id)


class Comment(BaseModel):
    content = db.StringField()
    like_count = db.IntField()
    user = db.ReferenceField('User')
    movie = db.ReferenceField('Movie', reverse_delete_rule=db.CASCADE)

    meta = {
        'indexes': [
            '-like_count'
        ]
    }

    @property
    def url(self):
        return COMMENT_URL.format(self.id)

    @property
    def user_url(self):
        return self.user.url

    @property
    def movie_url(self):
        return self.movie.url

    @classmethod
    def cache_by_key(cls, key, ids):
        cache.delete(key)
        cache.rpush(key, *ids)
        cache.expire(key, TIMEOUT)

    @classmethod
    def order_by_star(cls, start=0, limit=20):
        ids = cache.lrange(START_KEY, start, start+limit)
        if not ids:
            ids = [c.id for c in cls.objects.order_by('-like_count')[:TOTAL_SIZE]]
            cache.delete(START_KEY)
            cache.rpush(START_KEY, *ids)
            ids = ids[start: start+limit]
        return cls.get_multi(ids)

    def to_dict(self):
        movie_obj = self.movie
        user_obj = self.user

        movie = {
            'id': movie_obj.id,
            'name': movie_obj.name,
            'mark': movie_obj.mark,
            'url': movie_obj.url,
            'picture': movie_obj.picture
        }

        user = {
            'id': user_obj.id,
            'avatar': user_obj.picture,
            'name': user_obj.name,
        }

        return {
            'movie': movie,
            'user': user,
            'content': self.content,
            'like_count': self.like_count
        }


class User(BaseModel):
    name = db.StringField()
    picture = db.StringField()

    @property
    def url(self):
        return USER_URL.format(self.id)


class Process(BaseModel):
    STATUS = PENDING, SUCCEEDED, FAILLED = range(3)
    status = db.IntField(choices=STATUS, default=PENDING)

    @property
    def is_success(self):
        return self.status == self.SUCCEEDED

    def make_succeed(self):
        return self.update(status=self.SUCCEEDED)

    def make_fail(self):
        return self.update(status=self.FAILLED)


def search(subject_id, type):
    key = SEARCH_KEY.format(id=subject_id, type=type)
    if not subject_id:
        return []
    comment_id = cache.get(key)
    if comment_id:
        return Comment.get(comment_id)
    movie = None
    if type == "movie":
        movie = Movie.get(id=subject_id)
    if movie == None:
        return []

    comment = Comment.objects(movie=movie)[0]
    comment_id = comment.id
    if comment_id:
        cache.set(key, comment_id)
    return comment


def suggest(text):
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    key = SUGGEST_KEY.format(text=text)
    rs = cache.get(key)
    items = []
    if rs:
        temp_rs = ast.literal_eval(rs)
        for t in temp_rs:
            items.append(t[0])
        return items
    if not isinstance(text, unicode):
        text = text.decode('utf-8')
    movies = Movie.objects(name__contains=text)
    
    items.extend([{
        'id': movie.id, 'name': movie.name,
        'type': 'movie'}
    ] for movie in movies)
    cache.set(key, items)
    return items
