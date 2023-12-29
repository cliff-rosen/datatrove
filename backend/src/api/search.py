from common import db

def get_articles(PoI, DoI):
    rows = db.get_articles(PoI, DoI)
    for row in rows:
        row['date_pub'] = row['date_pub'].isoformat()

    return rows

