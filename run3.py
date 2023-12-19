import local_secrets as secrets
import pubmed_wrapper as pm
from openai import AsyncOpenAI
import asyncio
import xml.etree.ElementTree as ET


OPENAI_API_KEY = secrets.OPENAI_API_KEY
COMPLETION_MODEL = 'gpt-4-1106-preview'

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


async def main():
    tasks = [asyncio.create_task(go()) for _ in range(1)]
    print('about to await tasks...')
    results = await asyncio.gather(*tasks)
    print('back from task await')
    return results

sd = '2023/11/01'
ed = '2023/11/30'

print('starting')

res = pm.get_article_ids_by_date_range(sd, ed)
print(res['status_code'])
print(res['count'])
print(res['ids'][0:10])

res = pm.get_articles_from_ids(res['ids'][0:100])
print(res)

print('back')

#results = asyncio.run(main())
#print(results)
