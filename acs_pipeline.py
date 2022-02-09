# #import the needed libraries
# import os, sbol2, json, requests
# from sbol2 import BIOPAX_DNA, ComponentDefinition, Sequence, SBOL_ENCODING_IUPAC
# from sequences_to_features import FeatureLibrary
# from sequences_to_features import FeatureAnnotater



# #%%%

# def synbict_init(cwd):
#     # Load all library sbol files in the folder libraries
#     library_list = os.listdir(os.path.join(cwd, 'libraries'))
#     library_list = [os.path.join(cwd, 'libraries', x) for x in library_list] #list of file paths to sbol documents of libraries

#     feature_doc = []
#     for ind, library in enumerate(library_list):
#         feature_doc.append(sbol2.Document())
#         feature_doc[ind].read(library)

#     feature_library = FeatureLibrary(feature_doc)

#     # Annotate raw target sequence
#     min_feature_length = 40

#     annotater = FeatureAnnotater(feature_library, min_feature_length)
#     return(annotater)


# # # define collection creator
# # # not in use
# # def collection_creator(attachement):
# #     sbol_doc = sbol2.Document()

# #     #get title
# #     uri = attachement["uri"]
# #     response = requests.get(uri)
# #     title = response.text[response.text.find('div class="col-sm-8 entry-title')+37:]
# #     title = title[:title.find('</h1><h3>')]

# #     #create collection object
# #     paper_collect = sbol2.Collection(paper['displayId'])

# #     #add top level properties
# #     paper_collect.displayId = paper['displayId']
# #     try:
# #         paper_collect.description = paper['description']
# #     except:
# #         pass
# #     paper_collect.title = title
# #     p_source = paper['source']

# #     #add all of the annotation fields
# #     annot = paper['annotations']
# #     for ind1, an in enumerate(annot):
# #         if an['type']=='uri':
# #             setattr(paper_collect,f'an{ind1}',sbol2.URIProperty(paper_collect, an['name'], 0, 1,[]))
# #             setattr(paper_collect,f'an{ind1}',an['value'])
# #         if an['type']=='string':
# #             setattr(paper_collect,f'an{ind1}',sbol2.TextProperty(paper_collect, an['name'], 0, 1,[]))
# #             setattr(paper_collect,f'an{ind1}',an['value'])
# #     sbol_doc.addCollection(paper_collect)

#     # return (sbol_doc, paper_collect)

# #define sequence info puller
# def seq_file_reader(seq_file, sbol_doc, annotator, annotated_num=0):
#     problem_rows = []
#     molecule_type = BIOPAX_DNA
#     sbol_doc.addNamespace('https://wiki.synbiohub.org/wiki/Terms/synbiohub#', 'sbh')
        
#     with open(seq_file, 'rt') as names:
#         member_obj = []
#         #print(seq_file)
#         #split file based on > at the start of each information row
#         rows = names.read().split('>')
#         for i, row in enumerate(rows):
#             if len(row)>0:
#                 # print(row)
#                 #information row is separated by |
#                 if len([field.strip() for field in row.split('|')])==5:
#                     sequence_name, doi, pathname_of_file, seq_count, seq = [field.strip() for field in row.split('|')]
#                 else:
#                     problem_rows.append(row)
#                     continue
                

#                 sequence = "".join([field.strip() for field in seq.split('\n')])

#                 #create sbol files with dictionary entry
#                 articleID = pathname_of_file.split('/')[0]
#                 # name_use = check_name(articleID)
#                 component, annotated_num = synbict_use(sequence, f'{articleID}_{i}', annotator, annotated_num=annotated_num)
#                 component.wasGeneratedBy =  "https://synbiohub.org/public/sbksactivities/ACS_Synbio_Generation/1"
#                 component.wasDerivedFrom = f'https://doi.org/{doi}'
#                 file_type = pathname_of_file[pathname_of_file.rindex('.')+1:]
#                 component.supplementalFile = sbol2.URIProperty(component, 'https://wiki.synbiohub.org/wiki/Terms/synbiohub#supplementalFile', 0, 1, [])
#                 component.supplementalFileType = sbol2.URIProperty(component, 'https://wiki.synbiohub.org/wiki/Terms/synbiohub#supplementalFileType', 0, 1, [])
#                 # print(pathname_of_file, file_type)
#                 component.supplementalFile = pathname_of_file.replace(' ','_')
#                 component.supplementalFile = file_type
#                 # collect_obj.members += [component.identity]
                
#                 if sequence_name != "unknown" and sequence_name != "_unknown_seq":
#                     component.name= sequence_name

#                 #adding sequence
#                 sequence = sequence.lower() #removes spaces, enters, and makes all lower case
#                 sequence_obj = Sequence(f"{articleID}_{i}_sequence", sequence, SBOL_ENCODING_IUPAC)
#                 if sequence_name.strip() != "unknown":
#                     sequence_obj.name = f"{component.name} Sequence"
#                 sbol_doc.addSequence(sequence_obj)
#                 component.sequences = sequence_obj
#                 # collect_obj.members +=[sequence_obj.identity]

#                 sbol_doc.addComponentDefinition(component)
        
#     return(sbol_doc, annotated_num)

# #define synbict functionality
# def synbict_use(target_seq, seq_name, annotator, min_target_length=0, annotated_num=0):
#     annotated_list = annotator.annotate_raw_sequences(target_seq, seq_name, min_target_length)
#     # print(annotated_list)

#     if (len(annotated_list.componentDefinitions)-1)>0:
#         #print(len(annotated_list.componentDefinitions)-1)
#         annotated_num += 1
#     for comp in annotated_list.componentDefinitions:
#         if comp.displayId == f'{seq_name}_comp':
#             comp_out = comp
#     return(comp_out, annotated_num)
# #%%%

# #define variables
# cwd = os.getcwd()
# exist_list = []
# annotated_num = 0
# annotator = synbict_init(cwd)


# #make set of all sequence files
# seq_files = os.listdir(os.path.join(cwd, 'sequences-files'))[1:]
# seq_files = set([x.replace('.seq.txt', '') for x in seq_files])

# # make list of all papers
# ACS_doc = sbol2.Document()
# ACS_doc.read(os.path.join(cwd, 'ACS_collection_sbolnr.xml'))
# for col in ACS_doc.collections:
#     papers_list = list(col.members)
#     num_papers = len(papers_list)

# # # make list of all papers
# # with open(os.path.join(cwd,'test', 'ACS_collection.json'), 'r', encoding='utf-8') as file:
# #     papers_json = file.read()
# #     papers_json = json.loads(papers_json)

# ## 2190 annotated of 88,509 plus sb700461 (jiawei says 58055)
# ## loop through papers, if seq file exists make collection and run other two functions and add name to used_seq_files list
# for ind, paper in enumerate(papers_list):
#     if 0 <= ind <= 1554:
        
#         file_name = os.path.split(os.path.split(paper)[0])[1] #this is used to go from uri of the form: https://synbioks.org/public/ACS/sb5b00179/1 to just the sb5b00179 bit
#         file_path = os.path.join(cwd,'sequences-files', f'{file_name}.seq.txt')
#         print(f'ind: {ind}/{num_papers}', file_name)
#         if os.path.isfile(file_path):
#             with open(file_path) as file:
#                 # displayId = paper['displayId']
#                 #sbol_doc, collect_obj = collection_creator(paper)
#                 sbol_doc = sbol2.Document()
#                 sbol_doc, annotated_num = seq_file_reader(file_path, sbol_doc, annotator, annotated_num=annotated_num)
#                 # print(file.read())
#             exist_list.append(file_name)
#             sbol_doc.write(os.path.join(cwd, 'synbict_output', f'{file_name}.xml'))
# #make used_seqfiles list to set and check difference with all seq file set
# #exist_list=set(exist_list)
# #print(f'annotated_num: {annotated_num}')
# # print(seq_files.difference(exist_list))
