import json

orig_file_path = './PA_VTDs.json'
output_file_path = './PA_VTDs_clean.json'

with open(orig_file_path, 'r') as file:
    data = json.load(file)

nodes_array = data["nodes"]

data_to_keep = ["GEOID10", "STATEFP10", "COUNTYFP10", 
                "VTDST10", "2011_PLA_1", "TOT_POP", 
                "WHITE_POP", "BLACK_POP", "NATIVE_POP", 
                "ASIAN_POP", "HISP_POP", "PRES12D", 
                "PRES12R", "PRES12O", "id"]

cleaned_nodes = []
for node in nodes_array:
    cleaned_node = {key: node[key] for key in data_to_keep if key in node}
    cleaned_nodes.append(cleaned_node)
   
data["nodes"] = cleaned_nodes

# crate new file with modified data
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=2)

print(f"Cleaned file written to {output_file_path}")
