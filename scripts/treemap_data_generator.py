import json
import codecs
import os.path

data_dir = os.path.join("..", "data")

vital_file = open(os.path.join(data_dir, "vital.json"), "r")
vital_articles = json.load(vital_file)
languages = ['en', 'es', 'sw', 'zh', 'fr', 'my', 'ar', 'sv', 'ru', 'ja', 'ko', 'tr', 'de', 'pt', 'it']

# Needed to get native title
links_file = open(os.path.join(data_dir, "links.json"), "r")
links = json.load(links_file)
#links_file.close()

language_file = open(os.path.join(data_dir,  "language.json"), "r")
languages_dict = json.load(language_file)
#language_file.close() 

quality_dict = {}

for cat in vital_articles.keys():
    for subcat in vital_articles[cat].keys():
        for art in vital_articles[cat][subcat]:
            id = art['link'].replace("d:", "")
            quality_dict[id] = { 'title': art['title'], 'counts': {} }
            for lang in languages:
                filename = "../articles/" + lang + "/" + id + ".txt"
                if not os.path.isfile(filename):
                    quality_dict[id]['counts'][lang] = 0
                else:
                    f = open(os.path.join(data_dir, filename), "r")
                    text = f.read().decode('utf8')
                    quality_dict[id]['counts'][lang] = len(text)
                    if lang == 'zh':
                        quality_dict[id]['counts'][lang] *= 1.67
                    elif lang == 'ja' or lang == 'ko':
                        quality_dict[id]['counts'][lang] *= 1.5
                    f.close()

for id in quality_dict.keys():
    max_count = float(max(quality_dict[id]['counts'].values()))
    for lang in quality_dict[id]['counts'].keys():
        quality_dict[id]['counts'][lang] /= max_count

# Build treemap for each language
for lang in languages:
    treemap = { "categories": [] }

    for cat in vital_articles.keys():
        cat_node = {"name": cat, "subcategories": [] }
        for subcat in vital_articles[cat].keys():
            subcat_node = {"name": subcat, "articles": []}
            
            for art in vital_articles[cat][subcat]:
                id = art['link'].replace("d:", "")
                native_title = ""
                link = ""
                if lang in links[id].keys():
                    native_title = links[id][lang]["native_title"]
                    link = links[id][lang]["link"]
                
                article_node = {
                    "title": art["title"],
                    "quality": quality_dict[id]['counts'][lang],
                    "native_title": native_title,
                    "link": link
                }
                subcat_node['articles'].append(article_node)
            cat_node["subcategories"].append(subcat_node)

        treemap["categories"].append(cat_node)

    for node in languages_dict:
        if node["code"] == lang:
            treemap["language"] = node

    print lang
    output_file = open(os.path.join(data_dir, 
                       "quality_" + lang + ".json"), "w")
    json.dump(treemap, output_file, sort_keys=True, indent=4)
    output_file.close()
