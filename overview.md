1. Addgene is scrapped to pull all addgene ids. This was done via:
-addgene_idnums.py, however this poses problems as it seems not to page through all pages but repeat some. Ids scrapped output to addgene_id_list.csv
-addgene_url_tester.py, this is used next to systematically page through all numbers and check if the pages exist. Output to : addgene_url.csv

2. Next use excel to create a single list with no repeats of ids that exist based on the two csv files created above. This list is the addgene_combined_ids.csv

3. Then addgene_to_sbol.py is run. It pulls addgene info for ids found in addgene_combined_ids.csv between the numbers specified in line 177 and converts to sbol which is then output in the folder addgene_sbol. Any files which cause issues have their id number output to the file addgene_issues.csv

4. Next sbol_analysis.py is run to look at the metadata found in tags in the sbol files. (not needed but gives an overview of the addgene dataset)

5. Then manual analysis is carried out on the produced spreadsheets

6. Grounding was done using the species spreadsheet and addgene_species_grounding.py

7. Synbict analysis was carried out using addgene_synbict.py

8. An overview of the annotation results is carried out using annotation_overview.py and annotation_percentage.py

9. Files are uploaded using