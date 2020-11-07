from mysql import connector

import os

user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PWD')
database = os.environ.get('MYSQL_DATABASE')
host = os.environ.get('MYSQL_HOST')

def update_user(id_: str, AK: str, AS: str) -> None:
    try:
        cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        cur = cnx.cursor()

        sql = (
            "UPDATE accounts "
            "SET access_token=%s, access_secret=%s "
            "WHERE id=%s;"
        )
        cur.execute(sql, (AK, AS, id_))
        cnx.commit()

        cur.close()
        cnx.close()
    except Exception as e:
        print(e)

def update_query(id_:str, query: str) -> None:
    try:
        cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        cur = cnx.cursor()

        sql = (
            "UPDATE accounts "
            "SET query=%s"
            "WHERE id=%s;"
        )
        cur.execute(sql, (query, id_))
        cnx.commit()

        cur.close()
        cnx.close()
    except Exception as e:
        print(e)

def insert_user(id_: str, AK: str, AS: str) -> None:
    try:
        cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        cur = cnx.cursor()

        sql = (
            "INSERT INTO accounts VALUES (%s, %s, %s, NULL);"
        )
        cur.execute(sql, (id_, AK, AS))
        cnx.commit()

        cur.close()
        cnx.close()
    except Exception as e:
        print(e)

def is_exist(id_):
    try:
        cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        cur = cnx.cursor()

        sql = (
            "SELECT * FROM accounts WHERE id=%s;"
        )

        cur.execute(sql, (id_,))
        for val in cur:
            print(val)
            if val:
                cur.close()
                cnx.close()
                return True
        
        cur.close()
        cnx.close()
        return False
    
    except Exception as e:
        print(e)

def delete_user(id_) -> None:
    try:
        cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        cur = cnx.cursor()

        sql = (
            "DELETE FROM accounts WHERE id=%s;"
        )

        cur.execute(sql, (id_,))
        cnx.commit()
        
        cur.close()
        cnx.close()
    
    except Exception as e:
        print(e)

def fetch_all_users() -> list:
    try:
        cnx = connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )

        cur = cnx.cursor()

        results = list()
        sql = (
            "SELECT * FROM accounts;"
        )
        cur.execute(sql)
        for data in cur:
            results.append(data)

        cur.close()
        cnx.close()

        return results

    except Exception as e:
        print(e)
