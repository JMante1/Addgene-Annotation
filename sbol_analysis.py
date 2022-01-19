import os
import rdflib
import pandas as pd

files = os.listdir('addgene_sbol')
dir_path = os.path.dirname(os.path.realpath(__file__))
pred_file = os.path.join(dir_path, 'Analysis', 'all_predicates.txt')

with open(pred_file, 'r') as f:
    pred_list = f.read()
    pred_list.split(",")

print(type(pred_list))
# for p in pred_list:
#     print(p)

output_dict = {}
name_pred = 'bacterialResistances'
pred = rdflib.URIRef(f'https://www.addgene.org/{name_pred}')
all_addgene_predicates = False
for ind, file in enumerate(files):
    if 0 <= ind <= len(files):
        print(file, ind, len(files))
        g = rdflib.Graph()
        g.parse(os.path.join(dir_path, 'addgene_sbol', file))

        if all_addgene_predicates:
            add_gene_pred = {}
            # single_list = []
            for s, p, o in g:
                # list all addgene.org properties for the file
                if str(p).find('https://www.addgene.org/') >= 0:
                    pre = p.replace('https://www.addgene.org/', '')
                    add_gene_pred[pre] = 1
                    # if pre not in single_list:
                    #     single_list.append(pre)
            output_dict[file] = add_gene_pred
        else:
            for o in g.objects(predicate=pred):
                # prints the object property for the property specified above.
                output_dict[file] = o
if all_addgene_predicates:
    file_path_out = os.path.join(dir_path, 'Analysis','all_addgene_predicates.xlsx')
    df = pd.DataFrame.from_dict(output_dict, orient="index")
    # print(df)
    df.to_excel(file_path_out)
    # 
    # with open(file_path_out, 'w') as f:
    #     for key in output_dict.keys():
    #         val = str(output_dict[key]).replace("'", "").replace('[', '')
    #         val = val.replace(']', '')
    #         f.write(f'{key}, {val}\n')
    # print(single_list)
else:
    file_path_out = os.path.join(dir_path, 'Analysis', f'predicate_{name_pred}.csv')
    with open(file_path_out, 'w') as f:
        for key in output_dict.keys():
            # val = str(output_dict[key]).replace("'", "").replace('[', '')
            # val = val.replace(']', '')
            f.write(f'{key}, {output_dict[key]}\n')

# print(pd.DataFrame(output_dict))
        

# either pull term value from every file
# or pull all addgene terms from a file