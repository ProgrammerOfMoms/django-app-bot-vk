import pymysql.cursors

def connect():
    #try:
        cnx = pymysql.connect(
            user='a263932_1',
			password = 'azsxdcfr132',
            host = 'a263932.mysql.mchost.ru',
            #port = 3306,
            db='a263932_1'
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