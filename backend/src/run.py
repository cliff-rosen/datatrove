import urllib.request 
from xml.etree import ElementTree as ET
import common.pubmed_wrapper as pm
from common.pubmed_wrapper import Article

ids = ['22486366', '35858505', '38007612']
#ids = ['22486366']

articles = pm.get_articles_from_ids(ids)
for article in articles:
    print('==============================')
    print(article)

#citation = pm.get_citation_from_article(article)
#print(citation)

"""

get_articles_from_ids(ids)
    xml_res = get_articles(ids)
    articles = get_articles_as_element_list(xml_res)
    for article_node in articles:
        article = get_article_from_article_node(article_node)

        
raw xml -> xml node - > dict, array
    
"""