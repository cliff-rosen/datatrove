from common import db

def get_articles(PoI, DoI):
    rows = db.get_articles(PoI, DoI)
    for row in rows:
        row['comp_date'] = row['comp_date'].isoformat()

    return rows

