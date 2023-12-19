import local_secrets as secrets
from openai import AsyncOpenAI
import asyncio

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


print('starting')
results = asyncio.run(main())
print('back')
print(results)
