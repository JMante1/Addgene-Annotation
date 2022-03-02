import os
import re

cwd = os.getcwd()

# <sbol:elements>
file_list = os.listdir(os.path.join(cwd, 'addgene_sbol'))
seq_dict = {}
for ind, file in enumerate(file_list):
    if 0<= ind:
        with open(os.path.join(cwd, 'addgene_sbol', file), 'rt') as f:
            data = f.read()
        # print(data)
        seq = data[data.find("<sbol:elements>")+15:data.find("</sbol:elements>")]
        seq_len = len(seq)
        seq_dict[file] = seq_len
        print(f'{ind} of {len(file_list)} is {ind/len(file_list)}')

with open(os.path.join(cwd, 'Analysis', 'seq_lengths.txt'), 'w+') as f:
    f.write(str(seq_dict))