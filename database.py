import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv


load_dotenv()


def get_db():
    # mydb = psycopg2.connect(
    #   host=os.getenv("HOST"),
    #   port=os.getenv("PORT"),
    #   database=os.getenv("DATABASE"),
    #   user=os.getenv("USER"),
    #   password=os.getenv("PASSWORD")
    # )
    # mydb.autocommit = True
    # mycursor = mydb.cursor()
    # mycursor.execute(sql.SQL("CREATE DATABASE miniinternportal"))
    # mycursor.close()
    # mydb.close()

    mydb = psycopg2.connect(
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )
    
    mycursor_user = mydb.cursor()
    # mycursor_user.execute(sql.SQL("CREATE TABLE applicants (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), cv BYTEA, filename VARCHAR(255), status VARCHAR(255))"))
    # mycursor_user.close()
    
    mycursor_admin = mydb.cursor()
    # mycursor_admin.execute(sql.SQL("CREATE TABLE admin (id SERIAL PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"))
    # mycursor_admin.close()
    
    mydb.commit()
    return mydb, mycursor_user, mycursor_admin