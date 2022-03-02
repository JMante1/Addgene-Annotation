import os, sbol2
import pandas as pd

cwd = os.getcwd()



file_list = os.listdir(os.path.join(cwd, 'synbict_output'))
components_dict = {}
all_an_dict = {}
for ind, file in enumerate(file_list):
    if 0 <= ind:
        print(f'{ind} of {len(file_list)} {ind/len(file_list)}')
        doc = sbol2.Document()
        doc.read(os.path.join(cwd, 'synbict_output', file))
        


        for ind, comp in enumerate(doc.componentDefinitions):
            an_dict = {}
            
            seq_uri = comp.sequence
            sequence = doc.sequences[str(seq_uri)]
            len_seq = len(sequence)
            # print (comp)
            for an in comp.sequenceAnnotations:
                for loc in an.locations:
                    an_seq = sequence.elements[loc.start-1:loc.end-1]
                    percent_cover = '{:.2f}'.format(len(an_seq)/ (len_seq-1))
                    an_dict[an_seq] = {'an_name':an.name, 'an_len':len(an_seq), 'percent_cover':[percent_cover]}
                    if an_seq in all_an_dict:
                        all_an_dict[an_seq]['count'] +=1
                        all_an_dict[an_seq]['percent_cover'].append(percent_cover)
                    else:
                        all_an_dict[an_seq] = {'an_name':an.name, 'an_len':len(an_seq), 'count':1, 'percent_cover':[percent_cover]}
                    # print(an, loc.start, loc.end, an.name)
            
            components_dict[file]={'num_annotations':len(comp.sequenceAnnotations), 'annotation_dict':an_dict}
            # print(all_dict)
# print(components_dict)
df = pd.DataFrame.from_dict(components_dict, orient='index')
df.to_csv(os.path.join(cwd, 'Analysis', 'subparts_overview.csv'))
df.to_excel(os.path.join(cwd, 'Analysis', 'subparts_overview.xlsx'))

df1 = pd.DataFrame.from_dict(all_an_dict, orient='index')
df1.to_excel(os.path.join(cwd, 'Analysis', 'annotations_set.xlsx'))