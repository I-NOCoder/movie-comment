# -*- coding: utf-8 -*-


import sys

from utils import get_tree


MOVIE_URL = 'https://movie.douban.com/subject/{}/'
COMMENT_URL = 'https://movie.douban.com/subject/{}/comments?status=P'

reload(sys)
sys.setdefaultencoding("utf-8")


def parse_top250():
    pass


if __name__ == "__main__":
    parse_top250()