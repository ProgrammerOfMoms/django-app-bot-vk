import pymysql.cursors

def connect():
        cnx = pymysql.connect(
            user='',#enter your user
			password = '',#enter your password
            host = '',#enter your host
            port = 0,#enter port
            db=''#enter your database
        )
        return cnx

def executeSQL(sql, connection):
    with connection.cursor() as cursor:
        res = cursor.execute(sql)
        connection.commit()
        if res!=0:
            return list(cursor.fetchall())
        else:
            return 0
