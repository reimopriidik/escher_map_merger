import json
import pandas as pd

#########################
# Define the filenames! #
#########################
# Escher map
template_map='map.json'

# Reaction table (ModelSEED, Patric)
new_reaction_table='data.rxntbl'

#############################
#### Template Escher map ####
#############################
#Reads the old Escher map json
with open (template_map, 'r') as json_file:
    template_map_json = json.load(json_file)

#Changes gene_reaction_rule to 'nd'
for i in template_map_json[1]['reactions']:
    template_map_json[1]['reactions'][i]['gene_reaction_rule'] = 'nd'
del i

########################
#### New Escher map ####
########################
#Reads reaction table from the new Escher map
new_rxntbl = pd.read_csv(new_reaction_table, sep = '\t')

#######################################################
#### Adding the new annotation to the template map #### 
#######################################################
k=-1
#Loops through the reactions in new Escher .rxntbl
for i in new_rxntbl['ID']:
    k=k+1
    #Loops through the reactions mapped onto the template Escher map
    for j in template_map_json[1]['reactions']:
        #Looks if the two reactions are the same
        if template_map_json[1]['reactions'][j]['bigg_id']==i:
            #Writes new gene_reaction_rule to the template map (if the two reactions are the same)
            template_map_json[1]['reactions'][j]['gene_reaction_rule']=new_rxntbl['Genes'][k]
del k

##########################################
#### Saving the new map as .json file ####
##########################################
with open('map_with_new_genes.json', 'w') as outfile:
    json.dump(template_map_json, outfile)
