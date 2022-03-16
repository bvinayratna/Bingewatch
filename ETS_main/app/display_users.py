from sqlalchemy import create_engine

import pymysql

import pandas as pd

 

sqlEngine       = create_engine('mysql+pymysql://root:vinAy%402003@127.0.0.1/ets_database', pool_recycle=3600)

dbConnection    = sqlEngine.connect()

frame           = pd.read_sql("select * from ets_database.app_user", dbConnection);

 

pd.set_option('display.expand_frame_repr', False)

print(frame)

 

dbConnection.close()