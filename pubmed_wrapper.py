import requests
import xml.etree.ElementTree as ET
import urllib.parse


PUBMED_API_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_API_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
FILTER_TERM = "%28melanocortin%29%20OR%20%28natriuretic%29%20OR%20%28Dry%20eye%29%20OR%20%28Ulcerative%20colitis%29%20OR%20%28Crohn%E2%80%99s%20disease%29%20OR%20%28Retinopathy%29%20OR%20%28Retinal%20disease%29"
RETMAX = "10000"


def _get_date_clause(start_date, end_date):
    clause = 'AND (("<sdate>"[Date - Completion] : "<edate>"[Date - Completion]))'
    clause = clause.replace("<sdate", start_date)
    clause = clause.replace("<edate>", end_date)
    return urllib.parse.quote(clause)


def _get_date(article):
    pub_date = article.find(".//DateCompleted")
    year = pub_date.find("Year").text
    month_x = pub_date.find("Month")
    month = month_x.text if month_x is not None else '?'
    day_x = pub_date.find("Day")
    day = day_x.text if day_x is not None else '?'
    comp_date = f"{year}-{month}-{day}"
    return comp_date


def _get_article_from_xml(article):
    pmid = article.find(".//PMID").text
    print('pmid: ', pmid)
    title = article.find(".//ArticleTitle").text
    abstract_texts = article.findall('.//Abstract/AbstractText')
    abstract = ""
    for abstract_text in abstract_texts:
        abstract += ''.join(abstract_text.itertext())
    comp_date = _get_date(article)

    return [pmid, comp_date, title, abstract]


def get_article_ids_by_date_range(start_date, end_date):
    url = PUBMED_API_SEARCH_URL \
        + '?db=pubmed' \
        + '&term=%28' + FILTER_TERM + '%29' + _get_date_clause(start_date , end_date)\
        + '&retmax=' + RETMAX \
        + '&retmode=json'

    print(url)
    print('about to retrieve ids')
    response = requests.get(url)
    content = response.json()
    count = content['esearchresult']['count']
    ids = content['esearchresult']['idlist']

    return ({'status_code': response.status_code, 
             'count': count,
             'ids': ids})


def get_articles_from_ids(ids):

    articles = []

    batch_size = 100
    low = 0
    high = low + 100 - 1

    while low < len(ids):
        print(f"processing {low} to {high}")
        id_batch = ids[low: high]
        url = PUBMED_API_FETCH_URL + '?db=pubmed' + '&id=' + ','.join(id_batch)
        xml = ""
        try:
            response = requests.get(url)
            response.raise_for_status()
            xml = response.text
        except Exception as e:
            print("Error: ", e)

        root = ET.fromstring(xml)
        for article in root.findall(".//PubmedArticle"):
            articles.append(_get_article_from_xml(article))

        low += batch_size
        high += batch_size

    return articles



"""
url = PUBMED_API_SEARCH_URL \
    + '?db=pubmed' \
    + '&term=' + FILTER_TERM \
    + '&datetype=pdat' \
    + '&mindate=' + start_date \
    + '&maxdate=' + end_date \
    + '&retmax=' + RETMAX \
    + '&retmode=json'

article_dict = {
        'PMID': pmid,
        'Comp_Date': f"{year}-{month}-{day}",
        'Title': title,
        'Abstract': abstract
    }
"""
