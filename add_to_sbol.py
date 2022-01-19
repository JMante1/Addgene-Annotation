# import sbol2
import requests
from bs4 import BeautifulSoup as bsp
import sbol2
import io
import os
import pandas as pd
import asyncio
import aiohttp


async def addgene_to_sbol(session, addgene_id):
    url = f"https://www.addgene.org/{addgene_id}/"
    async with session.get(url) as response:
        assert response.status == 200
        return await response.read()

# PULL DATA ###############################################################################
async def pull_data(session, addgene_id):
    r = await addgene_to_sbol(session, addgene_id)
    print(addgene_id)
    # r = requests.get(url)
    # print(r.status_code)

    soup = bsp(r, 'html.parser')
    page_dict = {}

    try:
        page_dict['plasmid_title'] = soup.find_all('span', {'class':'material-name'})[0].string.strip()
        page_dict['addgene_id'] = soup.find_all('span', {'id':'addgene-item-id'})[0].string.strip()


        top_info = soup.find_all('div', {'class':'field'})
        for i in top_info:
            # print('$$$$$$$$$$$$$$$$$$$$')
            field_label = i.find_all('div', {'class':'field-label'})[0].string
            field_val = i.find_all('div', {'class':'field-content'})
            if len(field_val) > 0:
                # if field title is not sequence information
                field_val = field_val[0]
                if field_val.string is not None:
                    # pull field value
                    field_val = field_val.string.strip()
                else:
                    # deal with links
                    if field_val.a.string is not None:
                        field_val = {'href': f"https://www.addgene.org{field_val.a['href']}", 'link_text':field_val.a.string.strip()}
                    else:
                        field_val = {'href': f"https://www.addgene.org{field_val.a['href']}", 'link_text':field_val.a.cite.string.strip()}
            else:
                # for sequence information could be a list
                field_val = i.find_all('ul', {'class':'list-unstyled'})
                field_val1 = []
                for j in field_val:
                    link_val = j.find_all('div', {'id':'sequence_information'})[0].a['href']
                    field_val1.append(f'https://www.addgene.org{link_val}')
                field_val = field_val1

            page_dict[field_label] = field_val

        details = soup.find_all('section')
        for sec in details:
            # print("$$$$$$$$$$$$$$$$$$$") 
            if sec.h2 is not None:
                if sec.h2.span.string.strip() != "Ordering":
                    sec_items = sec.ul.find_all('li', {'class':'field'})
                    # sec_items1 = sec.ul.find_all('span', {'class':'field-label'})
                    for itm in sec_items:
                        if itm.div is not None:
                            item_label1 = itm.div.string.strip()
                            item_label = [x.strip() for x in item_label1.split(chr(10))]
                            item_label = " ".join(item_label)
                        else:
                            item_label1 = itm.span.string.strip()
                            item_label = [x.strip() for x in item_label1.split(chr(10))]
                            item_label = " ".join(item_label)
                        item_value = itm.text.replace(item_label1, "").replace("(Search Vector Database)", "").strip()
                        page_dict[item_label] = item_value

        citations = []
        for cite in soup.find_all('div', {'class':'indent well well-sm'}):
            cite = cite.small.text.split("\n")
            cite = [x.strip() for x in cite]
            cite = " ".join(cite)
            citations.append(cite)
        page_dict['ref_method'] = citations[0]
        page_dict['ref_bib'] = citations[1]


        # print(page_dict)
        ##################################### PULL ARTICLE INFORMATION #####################
        pub_link = page_dict['Publication']['href']
        r = requests.get(pub_link)
        pub_soup = bsp(r.text, 'html.parser')
        article_png = pub_soup.find_all('span', {'class':'glyphicon glyphicon-new-window'})[0]
        page_dict['Publication'] = article_png.parent['href']

        # $$$$$$$$$$$$$$$$$$$$$$$$$$PULL SEQUENCE$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        seq_info = page_dict['Sequence Information'][0]
        r = requests.get(seq_info)
        seq_soup = bsp(r.text, 'html.parser')
        gbk_url = seq_soup.find_all('a', {'class':'genbank-file-download'})[0]['href']
        r = requests.get(gbk_url)
        genbank_file = io.StringIO(r.content.decode()) # turn bytes to file type object

        request = { 'options': {'language' : 'SBOL2',
                                'test_equality': False,
                                'check_uri_compliance': False,
                                'check_completeness': False,
                                'check_best_practices': False,
                                'fail_on_first_error': False,
                                'provide_detailed_stack_trace': False,
                                'subset_uri': '',
                                'uri_prefix': 'www.examples.org',
                                'version': '',
                                'insert_type': False,
                                'main_file_name': 'genbank.gb',
                                        },
                    'return_file': True,
                    'main_file': genbank_file.read()
                }


        resp = requests.post("https://validator.sbolstandard.org/validate/", json=request)
        sbol_cont = resp.json()['result']
        # with open('sbol.xml', 'w') as f:
        #     f.write(sbol_cont)

        sbol_file = io.StringIO(sbol_cont)
        ####################### SBOL ADD PAGE DICT ##################################
        doc = sbol2.Document()
        doc.read(sbol_file)
        cd = doc.componentDefinitions[0]

        addgene_url = 'https://www.addgene.org/'
        doc.addNamespace(addgene_url, "addgene")


        setattr(cd, 'depositingLab', 
                    sbol2.URIProperty(cd, f'{addgene_url}depositingLab', '0', '*', [],
                                    initial_value=page_dict['Depositing Lab']['href']))

        setattr(cd, 'doi', 
                    sbol2.URIProperty(cd, f'{addgene_url}doi', '0', '*', [],
                                    initial_value=page_dict['Publication']))

        prop_dict = {}
        for prop in page_dict.keys():
            if prop not in ['Publication', 'Depositing Lab', 'Sequence Information']:
                prop_new = prop.replace("_", " ")
                prop_new = prop_new.replace("3", "three")
                prop_new = prop_new.replace('5', 'five')
                # A = 65, Z = 90, a=97, z=122
                next_upper = False
                prop_new2 = ''
                for ch in prop_new:
                    if ord(ch) == 32:
                        next_upper = True
                    elif 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
                        if next_upper:
                            prop_new2 += ch.upper()
                            next_upper = False
                        else:
                            prop_new2 += ch
                prop_new2 = prop_new2[0].lower() + prop_new2[1:]
                prop_dict[prop] = prop_new2

        for prop in prop_dict:
            prop_name = prop_dict[prop]
            setattr(cd, prop_name, 
                    sbol2.TextProperty(cd, f'{addgene_url}{prop_name}', '0', '*',
                                    initial_value=page_dict[prop]))


        # uri_prop = ['Growth Strain(s)', 'Cloning method']
        # for prop in uri_prop:
        #     print(page_dict[prop])
        cd.title = f'Addgene_{addgene_id}'
        doc.write(os.path.join('addgene_sbol', f'{addgene_id}_addgene_out.xml'))
        return addgene_id
    except:
        with open('addgene_issues.csv', 'a') as f:
            f.write(f'{addgene_id}\n')

################################# CREATE ALL SBOL FILES ##############################
# ids = [3, 4, 6]
async def main(min_i, max_i):
    async with aiohttp.ClientSession() as session:
        # add list of files in folder. and check what is in data but not folder
        data = pd.read_csv('addgene_combined_ids.csv', header=None).to_dict(orient='list')[0]
        problem_data = pd.read_csv('addgene_issues.csv', header=None).to_dict(orient='list')[0]
        conv_files = os.listdir(os.path.join(cwd, 'addgene_sbol'))
        conv_file_num = [int(x.replace('_addgene_out.xml', '')) for x in conv_files]
        conv_file_num = conv_file_num + problem_data
        files_to_do = [i for i in data if i not in conv_file_num]

        print('starting async pull')
        print(f'files to do: {len(files_to_do)}')
        
        ret = await asyncio.gather(*[pull_data(session, i) for i in files_to_do if min_i <= i < max_i])


min_i = 30000
max_i =  60000 #181796
cwd = os.getcwd()
asyncio.run(main(min_i, max_i))
