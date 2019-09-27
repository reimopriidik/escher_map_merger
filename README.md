# escher_map_merger
Little script that merges two Escher (https://github.com/zakandrewking/escher) maps into one file.

The code is not pretty and the commenting is poor but the script works.
Define the file names of two maps at the beginning of the script and then run in.
```python
#######
## Define the file names!
#######
template_map = 'map1.json'
new_map = 'map2.json'
```

Creates merged_map.json file as a result.

Note that the gene names (gene_reaction_rules) in the resulting map are from the original files.
So if you want to visualise expression data on the merged map then gene_reaction_rules must be changed before visualising the data.

# escher_gene_name_converter
Changes the gene names in Escher maps.
Define the file names of an Escher map and reaction table at the beginning of the script and then run in.
```python
#########################
# Define the filenames! #
#########################
# Escher map
template_map='map.json'

# Reaction table (ModelSEED, Patric)
new_reaction_table='data.rxntbl'
```

Reaction table (.rxntbl) file is as the one from ModelSEED.
````
ID        |Name                      |Equation                               |Definition                      |Genes
rxn00816  |Lactose galactohydrolase  |cpd00001+cpd00208<=>cpd00027+cpd00108  |H2O+LACT<=>D-Glucose+Galactose  |(fig|349741.147.peg.1993)
````

Creates merged_map.json file as a result.
