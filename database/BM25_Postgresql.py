import psycopg2
from BM25 import BM25Okapi
import pandas as pd

def search_bm25(query, connection):
    cursor = connection.cursor()

    cursor.execute("SELECT content, url FROM news")

    datacorpus = cursor.fetchall()

    df = pd.DataFrame(datacorpus, columns=['content', 'url'])
    corpus = df['content']

    tokenized_corpus = [doc.split(" ") for doc in corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.split(" ")

    doc_scores = bm25.get_scores(tokenized_query)
    bm25_output = bm25.get_top_n(tokenized_query, corpus, n = 1)

    cursor.close()
    connection.close()

    return bm25_output


if __name__ == "__main__":
    connection = psycopg2.connect(
        host="localhost",
        port = "5432",
        database="ViFactChecking",
        user="postgres",
        password="#Honganh123#"
)
    query = "Mỹ quyết liệt chinh phục lại châu Phi do sợ Nga và Trung Quốc"

    #query = input()

    print(type(search_bm25(query, connection)))

  
    
