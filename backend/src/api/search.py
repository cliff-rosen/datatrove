from common import db

def get_articles(batch, start_date, end_date, poi, doi):
    #poi = poi.lower()
    #doi = doi.lower()
    print(type(poi))
    rows = db.get_articles_filter(batch, start_date, end_date, poi, doi)
    for row in rows:
        row['comp_date'] = row['comp_date'].isoformat()

    return rows

