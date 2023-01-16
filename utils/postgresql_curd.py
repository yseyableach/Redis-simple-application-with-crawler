# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 09:38:15 2022
@author: Wits.JayYu
"""
# BLOB_FUNC()

import psycopg2
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Update connection string information
class postege_connect:
    # 建構式
    def __init__(self, host, dbname, user, password, sslmode, port):
        self.host = host  # 顏色屬性
        self.dbname = dbname  # 座位屬性
        self.user = user  # 座位屬性
        self.password = password  # 座位屬性
        self.sslmode = sslmode
        self.port = port

    def getDF(self, query):
        # Construct connection string
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4} port={5}".format(
            self.host, self.user, self.dbname, self.password, self.sslmode, self.port
        )
        conn = psycopg2.connect(conn_string)
        print("create connect")
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        result = pd.DataFrame(rows, columns=columns)
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def executeQuery(self, query):
        # Construct connection string
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4} port={5}".format(
            self.host, self.user, self.dbname, self.password, self.sslmode, self.port
        )
        conn = psycopg2.connect(conn_string)
        print("create connect")
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_df_to_db(self, df, table_Name):
        df = df.fillna(np.nan).replace([np.nan], [None])
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4} port={5}".format(
            self.host, self.user, self.dbname, self.password, self.sslmode, self.port
        )
        conn = psycopg2.connect(conn_string)
        print("create connect")
        cursor = conn.cursor()
        cols = ",".join(list(['"' + col + '"' for col in df.columns.tolist()]))
        query = (
            "INSERT INTO "
            + str(table_Name)
            + "("
            + str(cols)
            + ")"
            + " VALUES("
            + str(",".join(["%s" for i in range(len(df.columns))]))
            + ")"
        )
        # .fillna(np.nan).replace([np.nan], [None]) 很重要 nan , none是不一樣的
        tuples = [tuple(x) for x in df.values]
        print(query)
        print(tuples)
        """
        其實chunksize調大也行拉 但就看你的db能耐
        舉例以aws t2等級的
        每次5000筆是沒問題的
        https://aws.amazon.com/tw/rds/instance-types/
        但我很怕她爆掉所以我先設定1000
        """
        chunksize = 30000
        start = 0
        for i in range(0, len(tuples), chunksize):
            try:
                start = i
                end = i + chunksize
                print(start, (i + chunksize))
                cursor.executemany(query, tuples[start:end])
                conn.commit()
            except:
                end = i + chunksize
                cursor.executemany(query, tuples[end:])
                conn.commit()
        cursor.close()

    def sqlAchemyAppend(self, df, table_Name):
        connect_str = "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.password, self.host, self.port, self.dbname
        )
        psgengine = create_engine(connect_str)
        df.to_sql(
            table_Name, psgengine, if_exists="append", index=False, chunksize=10000
        )

    def returnsqlAchemyEngine(self):
        connect_str = "postgresql://{}:{}@{}:{}/{}".format(
            self.user, self.password, self.host, self.port, self.dbname
        )
        psgengine = create_engine(connect_str)
        return psgengine
