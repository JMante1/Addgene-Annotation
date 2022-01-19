import pandas as pd
import aiohttp
import asyncio
import time

data = pd.read_csv('addgene_combined_ids.csv', header=None).to_dict(orient='list')[0]

async def get(i, session):
    try:
        async with session.get(url=f'https://www.addgene.org/{i}') as response:
            with open('addgene_url1.csv', 'a') as f:
                f.write(f'{i}, {response.status}\n')
            print(f'{i}, {response.status}\n')
    except Exception as e:
        print(f"Unable to get url {f'https://www.addgene.org/{i}'} due to {e.__class__}.")


async def main(min_i, max_i):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(i, session) for i in range(min_i, max_i)])
    print(f"Finalized all. Return is a list of len {len(ret)} outputs.")

min_i = 169000
max_i = 170000
start = time.time()
asyncio.run(main(min_i, max_i))
end = time.time()

print(f"All websites tested. It took {end-start} seconds")

# # 28893
# for i in range(167718, 181795):  # 181795    # first number should be one more than last in file
#     if i not in data:
#         url = f'https://www.addgene.org/{i}'
#         r = requests.get(url)
#         with open('addgene_url1.csv', 'a') as f:
#             f.write(f'{i}, {r.status_code}\n')
#         print(i, r.status_code)
#     else:
#         print(i)