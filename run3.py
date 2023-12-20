import local_secrets as secrets
import pubmed_wrapper as pm
import gsheets as gs
from openai import AsyncOpenAI
import asyncio
import xml.etree.ElementTree as ET


OPENAI_API_KEY = secrets.OPENAI_API_KEY
COMPLETION_MODEL = 'gpt-4-1106-preview'
#SPREADSHEET_ID = '1cbU59j5_tkoflnlzT78QcBgHZDqC27yCCKsr5zvl8-I'
SPREADSHEET_ID = '1Wc8U2cVyTli-tssILDLKd7I15XGb2j5gKXx9CJ_QkWw'

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

messages = [{"role": "system", "content": "hello"}]


async def go():
    print('starting go')
    completion = await client.chat.completions.create(
        model=COMPLETION_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0
    )
    print('finishing go')
    return completion.choices[0].message.content


async def do_features():
    tasks = [asyncio.create_task(go()) for _ in range(1)]
    print('about to await tasks...')
    results = await asyncio.gather(*tasks)
    print('back from task await')
    return results

sd = '2023/11/01'
ed = '2023/11/30'

def main():

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
    gs.add_articles(articles)

    print('back')

main()

#print(pm.get_articles_from_ids(['38004229']))

#results = asyncio.run(main())
#print(results)
