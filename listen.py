
import redis
import pandas as pd 
from utils.postgresql_curd import postege_connect
r = redis.StrictRedis(host='localhost', port=6379, db=0)
Jay_PostgreSQLDB = postege_connect(
    host='127.0.0.1',
    dbname='db_name',
    user='postgres_n',
    password='postgres_p',
    sslmode='allow',
    port='5432',
)

sub = r.pubsub()
sub.subscribe('crawl')

for message in sub.listen():
    print('Got message', message)
    print(isinstance(message.get('data'), bytes))
    print(message['data'])

    decode_info = message['data']
    print(decode_info)

    if (
        isinstance(message.get('data'), bytes) and
        decode_info.decode() == 'GREETING'
    ):
        print('Hello')
    if (
        isinstance(message.get('data'), bytes) and
        message['data'].decode() == 'break'
    ):
        break
        
    if (
        isinstance(message.get('data'), bytes) and
        ("news" in decode_info.decode()) 
    ):
        try :
            def parse_url(url):
                import requests
                from bs4 import BeautifulSoup  
                title = []
                uuurl=[]
                res = requests.get(url)
                soup = BeautifulSoup(res.content, "lxml")
                soup = soup.find("div", class_="part_list_2")
                domian = "https://www.ettoday.net"
                for a,uuurl_ in zip(soup.find_all("h3"),soup.find_all("a")):
                    p = a.a.string
                    if p != None:
                        p = p.split('／')
                        uuurl.append(uuurl_['href'])
                        if len(p) > 1:
                            title.append(p[1])
                        else:
                            title.append(p[0])
                            
                return pd.DataFrame({'title': title ,'url':uuurl})
            infoDF = parse_url(message['data'].decode())
            Jay_PostgreSQLDB.insert_df_to_db(infoDF,'news')
            
        except Exception as e:
            print(e)

