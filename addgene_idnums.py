import requests
from bs4 import BeautifulSoup as bsp

for i in range(1, 2133):
    r = requests.get(f'https://www.addgene.org/search/catalog/plasmids/?q=&page_number={i}&page_size=50')
    id_soup = bsp(r.text, 'html.parser')
    id_boxes = id_soup.find_all('li', {'class':'list-group-item'})
    for box in id_boxes:
        id = box.article.div['id'].replace("Plasmids-", "")
        with open('addgene_id_list.csv', 'a') as f:
            f.write(f'{id}\n')
    print(i)
    # print(r.text)