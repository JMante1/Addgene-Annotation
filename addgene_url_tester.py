import requests

for i in range(1548, 2000):
    # first number should be one more than last in file
    url = f'https://www.addgene.org/{i}'
    r = requests.get(url)
    with open('addgene_url.csv', 'a') as f:
        f.write(f'{i}, {r.status_code}\n')
    print(i, r.status_code)