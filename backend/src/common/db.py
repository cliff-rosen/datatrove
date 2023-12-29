import pymysql.cursors
import json
import logging
import local_secrets as secrets

DB_SECRETS = secrets.DB_SECRETS

logger = logging.getLogger()

"""
domain: domain_id, domain_desc
document: doc_id, domain_id, doc_uri, doc_text
document_chunk: doc_chunk_id, doc_id, chunk_text, chunk_embedding
index: doc_chunk_id, embedding, metadata {sub_index: <SUB_INDEX>}
"""

##### CONNECTIONS #####


def get_connection():
    conn = pymysql.connect(
        user=DB_SECRETS["DB_USER"],
        password=DB_SECRETS["DB_PASSWORD"],
        host=DB_SECRETS["DB_HOST"],
        database=DB_SECRETS["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor)
    return conn


def close_connection(conn):
    conn.close()


def l_to_d(keys, values):
    return dict(zip(keys, values))

##### ARTICLES #####

def get_articles(PoI, DoI):
    conn = get_connection()
    cur = conn.cursor()
    query_text = """
        SELECT *
        FROM articles
        LIMIT 10
        """
    cur.execute(query_text)
    rows = cur.fetchall()
    close_connection(conn)
    return rows

