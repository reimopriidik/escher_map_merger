# escher_map_merger
Little script that merges two Escher (https://github.com/zakandrewking/escher) maps into one file.

The code is not pretty but the script works.
Define the map file names at the beginning of the script and then run in. Creates merged_map.json file.

Note that the gene names (gene_reaction_rules) in the resulting map are from the original files.
So if you want to visualise expression data on the merged map then gene_reaction_rules must be changed before visualising the data.
