import local_secrets as secrets
from openai import AsyncOpenAI
import openai
import logging
#from openai.embeddings_utils import get_embedding as openai_get_embedding


OPENAI_API_KEY = secrets.OPENAI_API_KEY
#COMPLETION_MODEL = 'gpt-3.5-turbo'
#COMPLETION_MODEL = 'gpt-4-32k'
COMPLETION_MODEL = 'gpt-4-1106-preview'
EMBEDDING_MODEL = "text-embedding-ada-002"
MAX_TOKENS = 400


logger = logging.getLogger(__name__)
logger.info('openai_wrapper loaded')

client = openai.OpenAI(api_key=OPENAI_API_KEY)
aclient = AsyncOpenAI(api_key=OPENAI_API_KEY)


def generate(messages, temperature=0, response_format='text'):
    print('generate start')
    response =''
    if response_format == 'text':
        rf = { "type": "text" }
    else:
         rf = { "type": "json_object" }

    try:
        completion = client.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            response_format=rf,
            temperature=temperature
            )
        response = completion.choices[0].message.content
    except Exception as e:
        print('query_model error: ', str(e))
        response = "ERROR"
        logger.error('agenerate error: ' + str(e))
        logger.error(messages)

    return response


async def agenerate(messages, temperature=0, response_format='text'):
    print('agenerate start')
    response =''

    if response_format == 'text':
        rf = { "type": "text" }
    else:
         rf = { "type": "json_object" }

    try:
        completion = await aclient.chat.completions.create(
            model=COMPLETION_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            response_format=rf,
            temperature=temperature
            )
        response = completion.choices[0].message.content
    except Exception as e:
        print('query_model error: ', str(e))
        response = "ERROR"
        logger.error('agenerate error: ' + str(e))
        logger.error(messages)

    print('agenerate done')
    return response


def get_embedding(text):
    res = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=text,
                    encoding_format="float"
                )
    return res.data[0].embedding
    
