#import the needed libraries
import os
import sbol2
import logging
import sequences_to_features as synbict_s2f


def synbict_init(cwd):
    # Load all library sbol files in the folder libraries
    library_list = os.listdir(os.path.join(cwd, 'libraries'))
    # list of file paths to sbol documents of libraries
    library_list = [os.path.join(cwd, 'libraries', x) for x in library_list]

    feature_doc = []
    for ind, library in enumerate(library_list):
        feature_doc.append(sbol2.Document())
        feature_doc[ind].read(library)

    feature_library = synbict_s2f.FeatureLibrary(feature_doc)

    return(feature_library)


cwd = os.getcwd()
addgene_sbol_list = os.listdir(os.path.join(cwd, 'addgene_sbol'))
feature_library = synbict_init(cwd)

logging.basicConfig(filename=os.path.join(cwd, 'synbict.log'), encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('synbict')

for ind, file in enumerate(addgene_sbol_list):
    if 2669 < ind:
        file_path_in = os.path.join(cwd, 'addgene_sbol', file)
        file_path_out = os.path.join(cwd, 'synbict_output', file)

        target_doc = synbict_s2f.load_target_file(file_path_in)
        target_library = synbict_s2f.FeatureLibrary([target_doc], False)

        output_docs = []
        output_library = synbict_s2f.FeatureLibrary(output_docs, False)

        synbict_s2f.curate(feature_library, target_library, output_library, [file_path_out], extend_features=False,
                       no_annotation=False, min_feature_length=40, min_target_length=40,
                       extension_threshold=0.05, extension_suffix='', in_place=True, minimal_output=False,
                       no_pruning=False, deletion_roles=[], cover_offset=14, delete_flat=False, auto_swap=True,
                       non_interactive=True, logger=logger, complete_matches=False, strip_prefixes=[])



        print(ind, len(addgene_sbol_list), ind/len(addgene_sbol_list), file)