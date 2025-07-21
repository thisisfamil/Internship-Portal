import psycopg2
from psycopg2 import sql


def get_db():
    # mydb = psycopg2.connect(
    #     host="localhost",
    #     port= "5432",
    #     database="postgres",
    #     user="postgres",
    #     password="Famil20070505"
    # )
    # mydb.autocommit = True
    # mycursor = mydb.cursor()
    # mycursor.execute(sql.SQL("CREATE DATABASE miniinternportal"))
    # mycursor.close()
    # mydb.close()

    mydb = psycopg2.connect(
        host="localhost",
        port="5432",
        database="miniinternportal",
        user="postgres",
        password="Famil20070505"
    )
    
    mycursor_user = mydb.cursor()
    # mycursor_user.execute(sql.SQL("CREATE TABLE applicants (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), cv BYTEA, filename VARCHAR(255), status VARCHAR(255))"))
    # mycursor_user.close()
    
    mycursor_admin = mydb.cursor()
    # mycursor_admin.execute(sql.SQL("CREATE TABLE admin (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"))
    # mycursor_admin.close()
    
    mydb.commit()
    return mydb, mycursor_user, mycursor_admin