# -*- coding: utf-8 -*-

import time

from utils import get_tree
from models import Movie, Comment, User, Process
from app import create_app

MOVIE_URL = 'https://movie.douban.com/subject/{}/'
COMMENT_URL = 'https://movie.douban.com/subject/{}/comments?status=P'


def unprocess_movie():
    create_app()
    unprocess = Process.objects.filter(status=Process.PENDING)
    return [p.id for p in unprocess]


def get_movie_info(movie_id):
    create_app()
    process = Process.get_or_create(id=movie_id)
    if process.is_success:
        return

    print 'Strting fetch movie: {}'.format(movie_id)
    start = time.time()
    process = Process.get_or_create(id=movie_id)

    movie = Movie.objects.filter(id=movie_id)
    if not movie:
        html = get_tree(MOVIE_URL.format(movie_id))
        name = html.xpath("//div[@id='content']//h1/span/text()")[0]
        mark = html.xpath("//div[@class='rating_wrap clearbox']//strong/text()")[0]
        picture = html.xpath("//div[@id='content']//div[@id='mainpic']//img/@src")[0]
        movie = Movie(id=movie_id, name=name, mark=mark, picture=picture)
        movie.save()
        get_top_comment_and_user_info(movie_id, movie)
        process.make_succeed()
        print 'Finished fetch movie: {} Cost: {}'.format(movie_id, time.time() - start)


def get_top_comment_and_user_info(comment_id, movie):
    create_app()
    comment = Comment.objects.filter(id=comment_id)
    if not comment:
        html = get_tree(COMMENT_URL.format(comment_id))
        content = html.xpath("//div[@id='content']//div[@class='comment-item']//div[@class='comment']//p/text()")[0]
        user_name = html.xpath("//div[@id='content']//div[@class='comment-item']//div[@class='avatar']//a/@title")[0]
        user_url = html.xpath("//div[@id='content']//div[@class='comment-item']//div[@class='avatar']//a/@href")[0]
        user_picture = html.xpath("//div[@id='content']//div[@class='comment-item']//div[@class='avatar']//a//img/@src")[0]
        like_count = html.xpath("//div[@id='content']//div[@class='comment-item']"
                                "//div[@class='comment']//span[@class='votes pr5']/text()")[0]
        user_id = user_url.split('/')[-2]
        user = User.get_or_create(id=user_id, name=user_name, picture=user_picture)
        user.save()
        comment = Comment.get_or_create(id=comment_id, content=content, like_count=like_count,
                                        user=user, movie=movie)
        comment.save()


if __name__ == "__main__":
    get_movie_info('1292052')
    get_top_comment_and_user_info('1292052')
