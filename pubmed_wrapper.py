import requests


PUBMED_API_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_API_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
FILTER_TERM = "%28melanocortin%29%20OR%20%28natriuretic%29%20OR%20%28Dry%20eye%29%20OR%20%28Ulcerative%20colitis%29%20OR%20%28Crohn%E2%80%99s%20disease%29%20OR%20%28Retinopathy%29%20OR%20%28Retinal%20disease%29"
RETMAX = "10000"


def get_article_ids_by_date_range(start_date, end_date):

    url = PUBMED_API_SEARCH_URL \
        + '?db=pubmed' \
        + '&term=' + FILTER_TERM \
        + '&datetype=pdat' \
        + '&mindate=' + start_date \
        + '&maxdate=' + end_date \
        + '&retmax=' + RETMAX \
        + '&retmode=json'

    print('about to retrieve ids')
    response = requests.get(url)
    content = response.json()
    count = content['esearchresult']['count']
    ids = content['esearchresult']['idlist']

    return ({'status_code': response.status_code, 
             'count': count,
             'ids': ids})


def get_articles_from_ids(ids):
    pass

#?db=pubmed&id=37409973&retmode=xml