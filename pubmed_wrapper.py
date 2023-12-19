import requests
import xml.etree.ElementTree as ET


PUBMED_API_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_API_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
FILTER_TERM = "%28melanocortin%29%20OR%20%28natriuretic%29%20OR%20%28Dry%20eye%29%20OR%20%28Ulcerative%20colitis%29%20OR%20%28Crohn%E2%80%99s%20disease%29%20OR%20%28Retinopathy%29%20OR%20%28Retinal%20disease%29"
RETMAX = "10000"


def get_article_ids_by_date_range(start_date, end_date):

    url = PUBMED_API_SEARCH_URL \
        + '?db=pubmed' \
        + '&term=%28' + FILTER_TERM + '%29' + get_date_clause(start_date , end_date)\
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

    url = PUBMED_API_FETCH_URL \
        + '?db=pubmed' \
        + '&id=' + ','.join(ids)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print("Error: ", e)

    xml = response.text
    x_print(xml)

    return response


def get_date(article):
    pub_date = article.find(".//PubDate")
    year = pub_date.find("Year")
    month = pub_date.find("Month")
    day = pub_date.find("Day")
    return year + '/' + month + '/' + day


def get_date_clause(start_date, end_date):
    clause = 'AND (("<sdate>"[Date - Completion] : "<edate>"[Date - Completion]))'
    clause = clause.replace("<sdate", start_date)
    clause = clause.replace("<edate>", end_date)
    return clause


def x_print(xml):
    root = ET.fromstring(xml)

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        #date = get_date(article)
        pub_date = article.find(".//DateCompleted")
        year = pub_date.find("Year").text
        month_x = pub_date.find("Month")
        month = month_x.text if month_x is not None else '?'
        day_x = pub_date.find("Day")
        day = day_x.text if day_x is not None else '?'
        print(f"PMID: {pmid}, Date: {year}/{month}/{day}")


    """
    url = PUBMED_API_SEARCH_URL \
        + '?db=pubmed' \
        + '&term=' + FILTER_TERM \
        + '&datetype=pdat' \
        + '&mindate=' + start_date \
        + '&maxdate=' + end_date \
        + '&retmax=' + RETMAX \
        + '&retmode=json'
    """
