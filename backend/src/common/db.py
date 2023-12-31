import pymysql.cursors
import json
import logging
import local_secrets as secrets

DB_SECRETS = secrets.DB_SECRETS

logger = logging.getLogger()


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
        LIMIT 20
        """
    cur.execute(query_text)
    rows = cur.fetchall()
    close_connection(conn)
    return rows

