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
    content = article[2] + '\n\n' + article[3]
    sys_msg = prompt + '\n\n<ABSTRACT>' + content + '</ABSTRACT>'
    messages =  [
        {"role": "system", "content": sys_msg}
      ]
    return messages


def get_features_from_json(feature_json):
    obj = json.loads(feature_json)

    """
    x = {
        "pathway_rel": obj.pathway_rel, 
        "disease_rel": obj.disease_rel,
        "is_systematic": obj.is_systematic,
        "study_type": obj.study_type,
        "study_outcome": obj.study_outcome,
        "relevant_pathways": obj.relevant_pathways,
        "relevant_diseases": obj.relevant_diseases
    }
    """

    obj['relevant_pathways'] = ", ".join(obj['relevant_pathways'])
    obj['relevant_diseases'] = ", ".join(obj['relevant_diseases'])
    obj['study_outcome'] = ", ".join(obj['study_outcome'])
    return list(obj.values())


async def update_features():
    print('starting')
    gs.google_auth(SPREADSHEET_ID)

    # get prompt and articles from sheet
    prompt = gs.get_prompt()
    articles = gs.get_articles()[0:2]

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
    gs.upload_articles(articles)


start_date = '2023/11/01'
end_date = '2023/11/30'
messages = [{"role": "system", "content": "hello"}]

asyncio.run(update_features())


# results = asyncio.run(main())
# print(results)


# load_articles_from_date_range(start_date, end_date)

# print(pm.get_articles_from_ids(['38004229']))

