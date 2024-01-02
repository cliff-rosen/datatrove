import logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import local_secrets as secrets
from common import db
from common.utils import get_score_from_features
import common.pubmed_wrapper as pm
import common.gsheets as gs
import common.openai_wrapper as model
import json
import asyncio
import xml.etree.ElementTree as ET
import time

OPENAI_API_KEY = secrets.OPENAI_API_KEY
COMPLETION_MODEL = 'gpt-4-1106-preview'
#SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'
#SPREADSHEET_ID = '1Wc8U2cVyTli-tssILDLKd7I15XGb2j5gKXx9CJ_QkWw'
SPREADSHEET_ID = '1my0yZpRRm5VJi5Zx-62saht4sSIa43zc--UMJnr0Inc'
FILTER_TERM = "(melanocortin) OR (natriuretic) OR (Dry eye) OR (Ulcerative colitis) OR (Crohn’s disease) OR (Retinopathy) OR (Retinal disease)"


logging.info('Starting')


def _get_messages(content):
    messages =  [
        {"role": "system", "content": content}
      ]
    return messages


def _get_features_from_json(article):
    (PMID, feature_json) = article
    if feature_json == "" or feature_json == 'ERROR':
        print ('get_features_from_json called with bad value')
        return ["ERROR","ERROR","ERROR","ERROR","ERROR","ERROR","ERROR"]
    obj = json.loads(feature_json)
    #print('---------------------------')
    #print(obj)

    if 'relevant_pathways' in obj:
        obj['relevant_pathways'] = ", ".join(obj['relevant_pathways'])
    else:
        obj['relevant_pathways'] = ""

    if 'relevant_diseases' in obj:
        obj['relevant_diseases'] = ", ".join(obj['relevant_diseases'])
    else:
        obj['relevant_diseases'] = ""

    if 'study_outcome' in obj:
        obj['study_outcome'] = ", ".join(obj['study_outcome'])
    else:
        obj['study_outcome'] = ""

    if 'pathway_rel' not in obj:
        obj["pathway_rel"]="ERROR"
    if 'disease_rel' not in obj:
        obj["disease_rel"]="ERROR"
    if 'is_systematic' not in obj:
        obj["is_systematic"]="ERROR"
    if 'study_type' not in obj:
        obj["study_type"]="ERROR"

    return {
        'PMID': PMID,
        'poi': obj["pathway_rel"], 
        'doi': obj["disease_rel"],
        'is_systematic': obj["is_systematic"],
        'study_type': obj["study_type"],
        'study_outcome': obj["study_outcome"],
        'poi_list': obj["relevant_pathways"],
        'doi_list': obj["relevant_diseases"]
    }


def load_articles_from_date_range(sd, ed):
    print('starting')

    # get article ids
    res = pm.get_article_ids_by_date_range(FILTER_TERM, sd, ed)
    ids = res['ids']
    print(res['status_code'])
    print(res['count'])
    print(res['ids'][0:10])

    # get articles from ids
    articles = pm.get_articles_from_ids(ids)

    # write articles to db
    db.insert_articles_bulk(articles, 1)

    print('back')


async def _do_generate_features(article, prompt):
    pmid = article['pmid']
    title = article['title']
    abstract = article['abstract']
    content = prompt + '<ABSTRACT>' + title + '\n' + abstract + '</ABSTRACT>'
    res = await model.agenerate(_get_messages(content), 0, 'json')
    return (pmid, res)


async def update_features():
    print('starting')
    articles_with_features = []

    # get prompt and articles from sheet
    gs.google_auth(SPREADSHEET_ID)
    prompt = gs.get_prompt()
    articles = db.get_articles_by_batch(BATCH)
    #articles = articles[0:10]

    # run articles through model to generate features
    batch_size = 200
    low = 0
    high = min(len(articles), low + batch_size)
    while low < len(articles):
        print(f"Running batch from {low} to {high}")
        tasks = [
            asyncio.create_task(_do_generate_features(articles[i], prompt))
            for i in range(low, high)
        ]
        print(' about to await tasks...')
        results = await asyncio.gather(*tasks)                 
        new_articles_with_features = [_get_features_from_json(results[i]) for i in range(0, len(results))]
        articles_with_features = articles_with_features + [new_articles_with_features]
        low += batch_size
        high = min(len(articles), low + batch_size)
        print(" back from running tasks")
        time.sleep(2)

    # write features back to db
    db.update_articles_features(new_articles_with_features)


def update_scores():
    scores = []
    gs.google_auth(SPREADSHEET_ID)

    print("restrieving articles")
    articles = gs.get_article_features()

    print("calculating scores")
    for article in articles:
        score = get_score_from_features(article)
        scores.append([score])

    print("updating scores")
    gs.upload_article_scores(scores)


async def _do_generate_summary(article, prompt):
    pmid = article['pmid']
    title = article['title']
    abstract = article['abstract']
    content = title + '\n' + abstract
    res = await model.agenerate(_get_messages(content), 0, 'text')
    return (pmid, res)


async def generate_summaries():
    print('starting')

    summaries = []
    # get prompt and articles from sheet
    #prompt = gs.get_prompt()
    prompt = "Create a two sentence summary of the following abstract: \n\n"
    articles = db.get_articles(1,1)

    articles = articles[0:20]

    # run articles through model
    batch_size = 10
    low = 0
    high = min(len(articles), low + batch_size)
    while low < len(articles):
        print(f"Running batch from {low} to {high}")
        tasks = [
            asyncio.create_task(_do_generate_summary(articles[i], prompt)) 
            for i in range(low, high)
        ]
        print(' about to await tasks...')
        results = await asyncio.gather(*tasks)                 
        new_rows = [(articles[i]['pmid'], results[i]) for i in range(0, len(results))]
        summaries += new_rows
        low += batch_size
        high = min(len(articles), low + batch_size)
        print(" back from running tasks")
        time.sleep(10)

    # update sheet with results
    
    print(summaries)


async def test():
    gs.google_auth(SPREADSHEET_ID)

    # get prompt and articles from sheet
    prompt = gs.get_prompt()
    articles = gs.get_articles()[0:1]

    # run articles through model
    tasks = [asyncio.create_task(model.agenerate(_get_messages(articles[i], prompt), 0, 'json')) for i in range(len(articles))]
    print('about to await tasks...')
    features = await asyncio.gather(*tasks)
    features_arr = [_get_features_from_json(features[i]) for i in range(len(features))]
    print(features_arr)
    print("back from running tasks")


BATCH = 1
start_date = '2023/11/01'
end_date = '2023/11/30'

# STEP 1: load articles in date range from PubMed to articles table
#load_articles_from_date_range(start_date, end_date)

# STEP 2: extract features from articles and write to Results
asyncio.run(update_features())

# STEP 3: update Results scores from features 
#update_scores()

# STEP x: generate and store summary
#asyncio.run(generate_summaries())

#asyncio.run(test())
# print(pm.get_articles_from_ids(['38004229']))

"""
res = pm.get_article_ids_by_date_range(FILTER_TERM, start_date, end_date)
ids = res['ids']
print(res['status_code'])
print(res['count'])
#print(res['ids'][0:10])


#ids = ['37960213']
articles = pm.get_articles_from_ids(ids)
for article in articles:
    print('------------------------------------')
    print(article)
    pmid = article.PMID
    title = article.title
    abstract = article.abstract
    comp_date = article.comp_date
    year = article.year
    authors = article.authors
    journal = article.journal
    volume = article.volume
    issue = article.issue
    medium = article.medium
    pages = article.pages
    db.update_articles_main(pmid, title, abstract, comp_date, year, 
                         authors, journal, volume, issue, medium, pages)
"""
