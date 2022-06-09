import pymysql
from config import user, password, db_name, host

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected...")
    print("#" *20)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            print(cursor.fetchall())
    finally:
        connection.close()

except Exception as ex:
    print("Connection failed")
    print(ex)

