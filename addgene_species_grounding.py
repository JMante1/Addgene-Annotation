import pandas as pd
import os

cwd = os.getcwd()

# assumes the header row is in row 10
grounding_terms = pd.read_excel(os.path.join(cwd, 'Analysis', 'predicate_species2.xlsx'), sheet_name='Original Output', skiprows=range(0,9), index_col=0)
grounding_dict = grounding_terms.to_dict()['Value']


# print(grounding_terms)
for ind, file in enumerate(grounding_dict.keys()):
    if 0 <= ind: # this is so that if it ran incompletely a new run can be done on the partial data set
        print(ind, len(grounding_dict.keys()), ind/len(grounding_dict.keys()))
        groundings = str(grounding_dict[file]).split("|")
        # print(file, groundings)
        grounding_text = ""
        for species in groundings:
            if species != 'Ungroundable':
                species_text = f'<sbh:sourceOrganism rdf:resource="http://purl.obolibrary.org/obo/NCBITaxon_{species}"/>\n'
                grounding_text += species_text
        if len(grounding_text)>0:
            with open(os.path.join(cwd, 'addgene_sbol', file), 'r+') as f:
                file_contents = f.read()
                file_contents = file_contents.replace('xmlns:dc="http://purl.org/dc/elements/1.1/"', 'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:sbh="https://wiki.synbiohub.org/wiki/Terms/synbiohub#"')
                file_contents = file_contents.replace('</addgene:species>\n', f'</addgene:species>\n{grounding_text}')
            with open(os.path.join(cwd, 'addgene_sbol', file), 'w') as f:
                f.write(file_contents)
        with open(os.path.join(cwd, 'grounded_files.csv'), 'a') as f:
                f.write(f'{file}\n')
