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

def get_articles_by_batch(batch):
    conn = get_connection()
    cur = conn.cursor()
    query_text = f"""
        SELECT *
        FROM articles
        WHERE batch = {batch}
        ORDER BY score desc
        LIMIT 20
        """
    cur.execute(query_text)
    rows = cur.fetchall()
    close_connection(conn)
    return rows

def get_articles_by_date(start_date, end_date, batch=1):
    conn = get_connection()
    cur = conn.cursor()
    query_text = f"""
        SELECT *
        FROM articles
        WHERE comp_date >= '{start_date}'
            AND comp_date <= '{end_date}'
            AND batch = {batch}
        ORDER BY score desc
        LIMIT 20
        """
    print(query_text)
    cur.execute(query_text)
    rows = cur.fetchall()
    close_connection(conn)
    return rows


def get_articles(PoI, DoI):
    conn = get_connection()
    cur = conn.cursor()
    query_text = """
        SELECT *
        FROM articles
        """
    cur.execute(query_text)
    rows = cur.fetchall()
    close_connection(conn)
    return rows


def insert_articles(pmid, title, abstract, comp_date, year,
                   authors, journal, volume, issue, medium, pages, batch=0):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                INSERT INTO articles (pmid, title, abstract, comp_date, year, authors, journal, volume, issue, medium, pages)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            record = (pmid, title, abstract, comp_date, year, authors, journal, volume, issue, medium, pages, batch)
            res = cursor.execute(query, record)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in insert:\n", str(e))
        raise

    return res


# articles is list of Article objects
def insert_articles_bulk(articles, batch=0):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                INSERT INTO articles (pmid, title, abstract, comp_date, year, authors, journal, volume, issue, medium, pages, batch)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            records = [(article.PMID, article.title, article.abstract,
                        article.comp_date, article.year, article.authors, 
                        article.journal, article.volume, article.issue,
                        article.medium, article.pages, batch) for article in articles]
            res = cursor.executemany(query, records)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in insert:\n", str(e))
        raise

    return res


def update_articles_main(pmid, title, abstract, comp_date, year, 
                         authors, journal, volume, issue, medium, pages):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                UPDATE articles
                SET title = %s, abstract = %s, comp_date = %s, year = %s, authors = %s, 
                    journal = %s, volume = %s, issue = %s, medium = %s, pages = %s
                WHERE pmid = %s
                """    
            record = (title, abstract, comp_date, year, authors, journal, volume, issue, medium, pages, pmid)
            res = cursor.execute(query, record)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update:\n", str(e))
        raise

    return res


# articles is list of Article dicts
def update_articles_features(articles):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                UPDATE articles
                SET poi = %s, doi = %s, is_systematic = %s,
                    study_type = %s, study_outcome = %s, poi_list = %s, doi_list = %s
                WHERE pmid = %s
                """    
            record = [(article['poi'], article['doi'], article['is_systematic'], article['study_type'], 
                       article['study_outcome'], article['poi_list'], article['doi_list'], article['PMID'])
                      for article in articles]
            res = cursor.executemany(query, record)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update\n", str(e))
        raise

    return res


def update_articles_summaries(articles):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                UPDATE articles
                SET summary = %s
                WHERE pmid = %s
                """    
            records = [(article['summary'], article['pmid']) 
                      for article in articles]
            res = cursor.executemany(query, records)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update\n", str(e))
        raise

    return res


def update_articles_scores(articles):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                UPDATE articles
                SET score = %s
                WHERE pmid = %s
                """    
            records = [(article['score'], article['pmid']) 
                      for article in articles]
            res = cursor.executemany(query, records)
            conn.commit()
    except Exception as e:
        print("***************************")
        print("DB error in update\n", str(e))
        raise

    return res

