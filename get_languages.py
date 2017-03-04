from bs4 import BeautifulSoup
import requests
import json

def clean_string(s):
    if ',' in s:
        s = s[:s.find(',')]
    if '(' in s:
        s = s[:s.find('(')]
    return s.rstrip()

language_list = []
url = 'https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes'
result = requests.get(url)
soup = BeautifulSoup(result.content)

language_table = soup.find("table", {"id": "Table"})
rows = language_table.find_all("tr")

for row in rows:
    cells = row.find_all("td")
    if len(cells)==0:
        continue

    english_name = cells[2].text
    native_name = cells[3].text
    code = cells[4].text
    language_list.append({'english_name': clean_string(english_name),
                        'native_name': clean_string(native_name),
                        'code': code})

with open('language.json', 'w') as fp:
    json.dump(language_list, fp)