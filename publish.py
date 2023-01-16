import redis
from postgresql_curd import postege_connect
# D:\milano_parse_long_long_long_three_API
r = redis.StrictRedis(host='localhost', port=6379, db=0)
u = 'https://www.ettoday.net/news/news-list-2023-01-04-1.htm'
