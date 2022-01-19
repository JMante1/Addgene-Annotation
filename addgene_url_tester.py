import requests
import pandas as pd

data = pd.read_csv('addgene_combined_ids.csv', header=None).to_dict(orient='list')[0]
data_error = pd.read_csv('addgene_404_ids.csv', header=None).to_dict(orient='list')[0]

# 28893
for i in range(0, 181798):  # 181795    # first number should be one more than last in file
    if i not in data and i not in data_error:
        url = f'https://www.addgene.org/{i}'
        r = requests.get(url)
        with open('addgene_url.csv', 'a') as f:
            f.write(f'{i}, {r.status_code}\n')
        print(i, r.status_code)
    else:
        print(i)