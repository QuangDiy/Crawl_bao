import psycopg2

def getConnection():
    conn =psycopg2.connect(
        host="localhost",
        database="ViFactChecking",
        user="postgres",
        password="#Honganh123#"
    )
    return conn

def InsertData(df,tablename):
    conn = getConnection()
    cur = conn.cursor()

    insertSql =f""" 

                insert into {tablename}(title,url,ncontent,des,topic,tenbao)
                values('{df['Title']}','{df['Link']}','{df['Topic']}','{df['Mô tả']}','{df['Nội dung']}','{df['Tên báo']}')

                 """
    cur.execute(insertSql)
    conn.commit()
    cur.close()
    conn.close()