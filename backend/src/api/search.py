from common import db

def get_articles(PoI, DoI):
    rows = db.get_articles_by_batch(1)
    for row in rows:
        row['comp_date'] = row['comp_date'].isoformat()

    return rows

