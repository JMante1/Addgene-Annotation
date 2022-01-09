import requests
import pandas as pd

data = pd.read_csv('addgene_combined_ids.csv', header=None).to_dict(orient='list')[0]

for i in range(10000, 11000):
    # first number should be one more than last in file
    if i not in data:
        url = f'https://www.addgene.org/{i}'
        r = requests.get(url)
        with open('addgene_url.csv', 'a') as f:
            f.write(f'{i}, {r.status_code}\n')
        print(i, r.status_code)
    else:
        print(i)