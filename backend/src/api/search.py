from common import db

def get_articles(start_date, end_date):
    print(start_date)
    rows = db.get_articles_by_date(start_date, end_date)
    for row in rows:
        row['comp_date'] = row['comp_date'].isoformat()

    return rows

