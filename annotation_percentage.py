import os, sbol2, json

cwd = os.getcwd()

file_list = os.listdir(os.path.join(cwd, 'synbict_output'))

# print(file_list)

out_dict = {}

for ind, file_name in enumerate(file_list):
    print(file_name, f'{ind} of {len(file_list)}')
    num_annotated = 0
    annotation_numbers = []
    doc_read = sbol2.Document()
    doc_read.read(os.path.join(cwd, 'synbict_output', file_name))
    for defin in doc_read.componentDefinitions:
        if len(defin.sequenceAnnotations) > 0:
            annotation_numbers.append(len(defin.sequenceAnnotations))
            num_annotated +=1
    out_dict[file_name] = [file_name, len(doc_read.componentDefinitions), num_annotated, annotation_numbers]
    print(out_dict[file_name])
print(out_dict)
with open(os.path.join(cwd, 'Analysis', 'annotation_number.txt'), 'w') as file:
     file.write(json.dumps(out_dict))