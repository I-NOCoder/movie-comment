# -*- coding: utf-8 -*-

import redis
from config import REDIS_HOST, REDIS_DB, REDIS_PORT

cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
