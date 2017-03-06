import json
import requests
import codecs
from bs4 import BeautifulSoup

"""
Script to get the text of all vital articles in a designated set of languages.
"""

languages = ['en', 'es', 'sw', 'zh', 'fr', 'my', 'ar']
f = open("links.json", "r") 
s = f.read()
tree = json.loads(s)

for lang in languages:
    for key in tree.keys():
        if lang in tree[key].keys():
            article_info = tree[key][lang]
            result = requests.get(article_info['link'])
            soup = BeautifulSoup(result.text, "lxml")
            content = soup.find("div", {"id": "content"})

            article_file = codecs.open("articles/" + lang + "/" + 
                key + ".txt", "w", "utf-8")
            article_file.write(content.text)
            article_file.close()
