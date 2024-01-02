import urllib.request 
from xml.etree import ElementTree as ET
import common.pubmed_wrapper as pm
from common.pubmed_wrapper import Article
from common import db
from common import gsheets as gs

"""
ids = ['22486366', '35858505', '38007612']
#ids = ['22486366']

articles = pm.get_articles_from_ids(ids)
for article in articles:
    print('==============================')
    print(article)

#citation = pm.get_citation_from_article(article)
#print(citation)
"""


"""

get_articles_from_ids(ids)
    xml_res = get_articles(ids)
    articles = get_articles_as_element_list(xml_res)
    for article_node in articles:
        article = get_article_from_article_node(article_node)

        
raw xml -> xml node - > dict, array
    
"""

article = 38017411

pmid = '56789a'
title = "Exploring the Depths of Neural Networks"
abstract = "This study delves into the intricate architectures and learning mechanisms of deep neural networks."
date_pub = "2023-06-15"
year = "2023"
authors = "Jane Doe, John Smith, Alex Johnson"
journal = "Journal of Artificial Intelligence Research"
volume = "29"
issue = "4"
medium = "Digital"
pages = "101-150"

poi = "yes"
doi = "no"
is_systematic = "Yes"
study_type = "Randomized Controlled Trial"
study_outcome = "Increased efficiency in neural network training"
poi_list = "XYZ123, ABC456, LMN789"
doi_list = "10.1000/j.ai.2023.06.001, 10.1000/j.ai.2023.06.002, 10.1000/j.ai.2023.06.003"
score = 85

print('start')
a = [1,2,3,4,5]
b = [6]
print(a + b)

#res = db.update_articles_main(pmid, title, abstract, date_pub, year, 
#                     authors, journal, volume, issue, medium, pages)
#res = db.update_articles_features(pmid, poi, doi, is_systematic, 
                             #study_type, study_outcome, poi_list, doi_list, score)
#res = db.insert_articles(pmid, title, abstract, date_pub, year, 
#                     authors, journal, volume, issue, medium, pages)
#print(res)