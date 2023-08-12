import psycopg2
import csv

connection = psycopg2.connect(
        host="localhost",
        port = "5432",
        database="ViFactChecking",
        user="postgres",
        password="#Honganh123#"
)


# host="localhost",
# port="5432",
# database="FactCheck",
# user="postgres",
# password="tranquangduy1810"

cursor = connection.cursor()

csv_file_path = "datanews9k.csv"

with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        title = row[0] 
        description = row[1]
        content = row[2]
        topic = row[3]
        url = row[5]
        date_publish = None
    
        insert_query = "INSERT INTO news (url, title, description, content, topic, date_publish) VALUES (%s, %s, %s, %s, %s, %s)"  
        data = (url, title, description, content, topic, date_publish)
        cursor.execute(insert_query, data)

connection.commit()

cursor.close()
connection.close()
