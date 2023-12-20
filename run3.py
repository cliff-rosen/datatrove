import logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from utils import get_score_from_features
import local_secrets as secrets
import pubmed_wrapper as pm
import gsheets as gs
import openai_wrapper as model
import json
import asyncio
import xml.etree.ElementTree as ET


OPENAI_API_KEY = secrets.OPENAI_API_KEY
COMPLETION_MODEL = 'gpt-4-1106-preview'
#SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'
SPREADSHEET_ID = '1Wc8U2cVyTli-tssILDLKd7I15XGb2j5gKXx9CJ_QkWw'


logging.info('Starting')


def load_articles_from_date_range(sd, ed):

    print('starting')

    # get article ids
    res = pm.get_article_ids_by_date_range(sd, ed)
    ids = res['ids']
    print(res['status_code'])
    print(res['count'])
    print(res['ids'][0:10])

    # get articles from ids
    articles = pm.get_articles_from_ids(ids)

    # write articles to sheet
    gs.google_auth(SPREADSHEET_ID)
    gs.upload_articles(articles)

    print('back')


def get_messages(article, prompt):
    if len(article) == 3: # missing abstract
        article.append('')
    content = article[2] + '\n\n' + article[3]
    sys_msg = prompt + '\n\n<ABSTRACT>' + content + '</ABSTRACT>'
    messages =  [
        {"role": "system", "content": sys_msg}
      ]
    return messages


def get_features_from_json(feature_json):
    if feature_json == "" or feature_json == 'ERROR':
        print ('get_features_from_json called with bad value')
        return ["ERROR","ERROR","ERROR","ERROR","ERROR","ERROR","ERROR"]
    obj = json.loads(feature_json)

    print('---------------------------')
    print(obj)
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

    return [
        obj["pathway_rel"], 
        obj["disease_rel"],
        obj["is_systematic"],
        obj["study_type"],
        obj["study_outcome"],
        obj["relevant_pathways"],
        obj["relevant_diseases"]
    ]


async def update_features():
    print('starting')
    gs.google_auth(SPREADSHEET_ID)

    # get prompt and articles from sheet
    prompt = gs.get_prompt()
    articles = gs.get_articles()

    # run articles through model
    tasks = [asyncio.create_task(model.agenerate(get_messages(articles[i], prompt), 0, 'json')) for i in range(len(articles))]
    print('about to await tasks...')
    features = await asyncio.gather(*tasks)
    features_arr = [get_features_from_json(features[i]) for i in range(len(features))]
    print(features_arr)
    print("back from running tasks")

    # update sheet with results
    articles = [list(pair[0] + pair[1]) for pair in zip(articles, features_arr)]
    print(articles)
    gs.upload_articles_with_features(articles)


async def test():
    gs.google_auth(SPREADSHEET_ID)

    # get prompt and articles from sheet
    prompt = gs.get_prompt()
    articles = gs.get_articles()[0:1]

    # run articles through model
    tasks = [asyncio.create_task(model.agenerate(get_messages(articles[i], prompt), 0, 'json')) for i in range(len(articles))]
    print('about to await tasks...')
    features = await asyncio.gather(*tasks)
    features_arr = [get_features_from_json(features[i]) for i in range(len(features))]
    print(features_arr)
    print("back from running tasks")


async def update_features_slow():
    print('starting')
    gs.google_auth(SPREADSHEET_ID)

    # get prompt and articles from sheet
    prompt = gs.get_prompt()
    articles = gs.get_articles()
    #articles = articles[0:2]

    # run articles through model
    features = []
    for i in range(len(articles)):
        print('processing articles ', i)
        features_json = model.generate(get_messages(articles[i], prompt), 0, 'json')
        features_arr = get_features_from_json(features_json)
        print(features_arr)
        features.append(features_arr)

    # update sheet with results
    articles = [list(pair[0] + pair[1]) for pair in zip(articles, features)]
    print(articles)
    gs.upload_articles_with_features(articles)



start_date = '2023/11/01'
end_date = '2023/11/30'
messages = [{"role": "system", "content": "hello"}]

#asyncio.run(test())
#asyncio.run(update_features())
asyncio.run(update_features_slow())

# results = asyncio.run(main())
# print(results)


# load_articles_from_date_range(start_date, end_date)

# print(pm.get_articles_from_ids(['38004229']))

