import urllib.request 
from xml.etree import ElementTree

def pubmed_search(keyword):
    ids = []
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {'db':'pubmed',
              'term':keyword,
              'retmode':'xml'}
    url = base_url + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as f:
        root = ElementTree.fromstring(f.read())
        
    for id_tag in root.iter('Id'):
        ids.append(id_tag.text)
        
    return ids

def fetch_details(id):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    params = {'db':'pubmed',
              'id':id,
              'retmode':'xml'}
    url = base_url + '?' + urllib.parse.urlencode(params)  
    with urllib.request.urlopen(url) as f:
        data = f.read() 
        # parse XML response to extract needed fields
        ...

def run1():        
    keyword_list = [
            'Dry eye disease',
            'Ulcerative colitis',
            'Crohn’s disease',
            'Retinopathy',
            'Retinal disease'
            ]       

    results = pubmed_search(keyword_list[0])


i = [1,2,3]
for j in range(len(i)):
    print(j)

'''
for result_id in results:
    details = fetch_details(result_id)
    print(details)
'''