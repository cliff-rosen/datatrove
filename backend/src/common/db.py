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


#def update_articles(pmid, title, abstract, date_pub, year, authors, journal, volume, issue, medium, pages, poi, doi, is_systematic, study_type, study_outcome, poi_list, doi_list, score):


def insert_articles(pmid, title, abstract, date_pub, year,
                   authors, journal, volume, issue, medium, pages):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:

            query = """
                INSERT INTO articles (pmid, title, abstract, date_pub, year, authors, journal, volume, issue, medium, pages)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            record = (pmid, title, abstract, date_pub, year, authors, journal, volume, issue, medium, pages)
            res = cursor.execute(query, record)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in insert:\n", str(e))
        raise

    return res



def update_articles_main(pmid, title, abstract, date_pub, year, 
                         authors, journal, volume, issue, medium, pages):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:

            query = """
                UPDATE articles
                SET title = %s, abstract = %s, date_pub = %s, year = %s, authors = %s, 
                    journal = %s, volume = %s, issue = %s, medium = %s, pages = %s
                WHERE pmid = %s
                """    
            record = (title, abstract, date_pub, year, authors, journal, volume, issue, medium, pages, pmid)
            res = cursor.execute(query, record)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update:\n", str(e))
        raise

    return res


def update_articles_features(pmid, poi, doi, is_systematic, 
                             study_type, study_outcome, poi_list, doi_list, score):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:

            query = """
                UPDATE articles
                SET poi = %s, doi = %s, is_systematic = %s,
                    study_type = %s, study_outcome = %s, poi_list = %s, doi_list = %s, score = %s
                WHERE pmid = %s
                """    
            record = (poi, doi, is_systematic, 
                             study_type, study_outcome, poi_list, doi_list, score, pmid)
            res = cursor.execute(query, record)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update\n", str(e))
        raise

    return res

