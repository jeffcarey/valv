import json
import requests
from bs4 import BeautifulSoup

"""
Extracts links for each vital article, for each language available
Creates a json structure with the article id (QXXX) as the top level key,
then with the language code as the key for each inner node. The inner
nodes have keys 'native_title' and 'link'.
"""


url_base = 'https://www.wikidata.org/wiki/'
LIST_TAG = "wikibase-sitelinklistview-listview"
topic_file = open("vital.json", "r")
s = topic_file.read()
topic_tree = json.loads(s)
link_dict = {}

for cat in topic_tree.keys():
    for subcat in topic_tree[cat].keys():
        for article in topic_tree[cat][subcat]:
            topic_dict = {}
            
            link_id = article['link'].replace("d:","")

            data_page = requests.get(url_base + link_id)
            soup = BeautifulSoup(data_page.content, "lxml")

            link_lists = soup.find_all("ul", {"class": LIST_TAG})
            wiki_link_list = link_lists[0]
            items = wiki_link_list.find_all("li")
            for li in items:
                
                d = { 'link': li.a['href'],
                     'native_title': li.a.text
                     }
                topic_dict[li.a['hreflang']] = d

            link_dict[link_id] = topic_dict

with open("links.json", "w") as f:
    json.dump(link_dict, f, sort_keys=True, indent=4)
