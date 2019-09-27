import json
import pandas as pd

#######
## Define the file names!
#######
template_map = 'map1.json'
new_map = 'map2.json'

#######
## reads the files and puts the data into dictionaries and a data frame
#######
#reads the two maps as json file
with open (new_map, 'r') as json_file:
    new_map = json.load(json_file)
    
with open (template_map, 'r') as json_file:
    template_map = json.load(json_file)
    
#rxn dict
#creates a list of new rxn keys for temp map
new_keys = list(range(int((list((new_map[1]['reactions'].keys()))[len(new_map[1]['reactions'].keys())-1]))+1,len(
    template_map[1]['reactions'])+int((list((new_map[1]['reactions'].keys()))[len(new_map[1]['reactions'].keys())-1]))+1,1)) 

#puts temp rxn-s into new dict with new rxn keys
new_temp_rxn = dict()
for i in range(0,len(new_keys),1):
    new_temp_rxn[str(new_keys[i])] = template_map[1]['reactions'][list(template_map[1]['reactions'].keys())[i]]
del i, new_keys

#node dict
#created dataframe of old vs new node keys
nodes_table = pd.DataFrame({'old_nodes':list(template_map[1]['nodes'].keys()),
                            'new_nodes':list(range(int(list(new_map[1]['nodes'].keys())[len(new_map[1]['nodes'].keys())-1])+1,len(template_map[1]['nodes'].keys())+int(list(new_map[1]['nodes'].keys())[len(new_map[1]['nodes'].keys())-1])+1,1))
})

#puts temp nodes into new dict with new node keys
new_temp_nodes = dict()
for i in range(0,len(nodes_table['new_nodes'].tolist()),1):
    new_temp_nodes[str(nodes_table['new_nodes'].tolist()[i])] = template_map[1]['nodes'][nodes_table['old_nodes'].tolist()[i]]
del i

#combined dict
new_rxn_nodes = dict()
new_rxn_nodes['reactions'] = new_temp_rxn
new_rxn_nodes['nodes'] = new_temp_nodes

#######
## positioning the template_map below new_map
#######
y_coef = list()
for i in new_map[1]['reactions']:
    y_coef.append(new_map[1]['reactions'][i]['label_y'])
del i
y_coef=max(y_coef)+5000

#changes y-coordinates for reactions and reactions.segments (b1 and b2)
for i in template_map[1]['reactions']:
    template_map[1]['reactions'][i]['label_y']=template_map[1]['reactions'][i]['label_y']+y_coef
    for j in template_map[1]['reactions'][i]['segments']:
        if template_map[1]['reactions'][i]['segments'][j]['b1'] == None:
            pass
        else:
            template_map[1]['reactions'][i]['segments'][j]['b1']['y']=template_map[1]['reactions'][i]['segments'][j]['b1']['y']+y_coef
        if template_map[1]['reactions'][i]['segments'][j]['b2'] == None:
            pass
        else:
            template_map[1]['reactions'][i]['segments'][j]['b2']['y']=template_map[1]['reactions'][i]['segments'][j]['b2']['y']+y_coef
del i

#changes y-coordinates for nodes
for i in template_map[1]['nodes']:
    template_map[1]['nodes'][i]['y'] = template_map[1]['nodes'][i]['y'] + y_coef
    if 'label_y' in list(template_map[1]['nodes'][i].keys()):
        template_map[1]['nodes'][i]['label_y'] = template_map[1]['nodes'][i]['label_y'] + y_coef
    else:
        pass
del i

#changes y-coordinates for text labels
if len(list(template_map[1]['text_labels']))>0:
    for i in template_map[1]['text_labels']:
        template_map[1]['text_labels'][i]['y'] = template_map[1]['text_labels'][i]['y'] + y_coef
    del i, y_coef

#######
## merging the two json map dicts
#######
#changes segments.keys() and puts everything into segments_new
new_seg = int(list(new_map[1]['reactions'][list(new_map[1]['reactions'])[-1]]['segments'])[-1])+1
for i in list(new_rxn_nodes['reactions'].keys()):
    new_temp_rxn[i]['segments_new'] = dict()
    for old_seg in list(new_rxn_nodes['reactions'][i]['segments'].keys()):
        new_rxn_nodes['reactions'][i]['segments_new'][str(new_seg)] = new_rxn_nodes['reactions'][i]['segments'][str(old_seg)]
        new_seg=new_seg+1
del i, new_seg, old_seg

#rewrites segments and deletes segements_new
for i in list(new_rxn_nodes['reactions'].keys()):
    new_rxn_nodes['reactions'][i]['segments'] = new_rxn_nodes['reactions'][i]['segments_new']
del i

for i in list(new_rxn_nodes['reactions'].keys()):
    del new_rxn_nodes['reactions'][i]['segments_new']
del i

#changes template_map[1]['reactions'][key]['segments'][key]['from_node_id']
for i in list(new_rxn_nodes['reactions'].keys()):
    for seg in list(new_rxn_nodes['reactions'][i]['segments'].keys()):
        new_rxn_nodes['reactions'][i]['segments'][seg]['from_node_id'] = str(list(nodes_table['new_nodes'][nodes_table.index[nodes_table['old_nodes'] == new_rxn_nodes['reactions'][i]['segments'][seg]['from_node_id']].tolist()])[0])
del i, seg

#changes template_map[1]['reactions'][key]['segments'][key]['to_node_id']
for i in list(new_rxn_nodes['reactions'].keys()):
    for seg in list(new_rxn_nodes['reactions'][i]['segments'].keys()):
        new_rxn_nodes['reactions'][i]['segments'][seg]['to_node_id'] = str(list(nodes_table['new_nodes'][nodes_table.index[nodes_table['old_nodes'] == new_rxn_nodes['reactions'][i]['segments'][seg]['to_node_id']].tolist()])[0])
del i, seg

#merges text_labels into new_rxn_nodes dict
if len(list(new_map[1]['text_labels'].keys()))>0:
    if len(list(template_map[1]['text_labels'].keys()))>0:
        #both new and template map have text_labels
        new_rxn_nodes['text_labels'] = new_map[1]['text_labels']
        for i in template_map[1]['text_labels']:
            new_rxn_nodes['text_labels'][str(int(list(new_rxn_nodes['text_labels'].keys())[-1])+1)] = template_map[1]['text_labels'][i]
        del i
    else:
        #only new map has text_labels
        new_rxn_nodes['text_labels'] = new_map[1]['text_labels']
else:
    #only template map has text_labels
    new_rxn_nodes['text_labels'] = template_map[1]['text_labels']

#merges two maps into one dict
for k in new_map[1]:
     new_map[1][k].update(new_rxn_nodes.get(k, {}))
del k

#######
## resizing the canvas
#######
x_axis = list()
y_axis = list()
for i in new_map[1]['reactions']:
    x_axis.append(new_map[1]['reactions'][i]['label_x'])
    y_axis.append(new_map[1]['reactions'][i]['label_y'])
del i

new_map[1]['canvas']['x'] = min(x_axis)-2000
new_map[1]['canvas']['y'] = min(y_axis)-2000
new_map[1]['canvas']['width'] = max(x_axis)-min(x_axis)+4000
new_map[1]['canvas']['height'] = max(y_axis)-min(y_axis)+4000
del x_axis, y_axis

#######
## saving the new map as merged_map.json
#######
with open('merged_map.json', 'w') as f:
        json.dump(new_map, f)
