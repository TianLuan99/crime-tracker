from flask import Flask
from mysql.connector import pooling
import os
from yaml import load, Loader

def init_db_engine() -> pooling.MySQLConnectionPool:
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]


    # Create a connection pool
    db = pooling.MySQLConnectionPool(pool_name='backend-pool',
                                        pool_size=32,
                                        user=os.environ.get('MYSQL_USER'),
                                        password=os.environ.get('MYSQL_PASSWORD'),
                                        host=os.environ.get('MYSQL_HOST'),
                                        database=os.environ.get('MYSQL_DB'))    
    return db

db = init_db_engine()
