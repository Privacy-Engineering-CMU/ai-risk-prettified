import pandas as pd
import json
import random

def load_resources(file_path):
    resource_df = pd.read_csv(file_path, usecols=['QuickRef', 'URL'])
    return {row[0].strip(): row[1].strip() for row in resource_df.values 
            if isinstance(row[0], str) and isinstance(row[1], str)}

def process_risk_data(file_path, resources_urls):
    df = pd.read_csv(file_path)
    column_names = list(df.columns)
    listed_json = []

    for idx, row in enumerate(df.values):
        dict_rep = {c: v for c, v in zip(column_names, row)}
        dict_rep = clean_dict_rep(dict_rep, resources_urls)
        
        if any(char.isalpha() for char in dict_rep['Ev_ID']):
            continue
        
        listed_json.append(dict_rep)

    return listed_json

def clean_dict_rep(dict_rep, resources_urls):
    columns_to_remove = ['Paper_ID', 'Cat_ID', 'SubCat_ID', 'AddEv_ID', 'Category level', 'Additional ev.', 'P.Def', 'p.AddEv']
    for column in columns_to_remove:
        dict_rep.pop(column, None)

    if isinstance(dict_rep.get('Additional ev.'), str) and isinstance(dict_rep.get('Description'), str):
        dict_rep['Description'] = f"{dict_rep['Description']}\nAdd.: {dict_rep['Additional ev.']}"

    dict_rep['QuickRef'] = (dict_rep['QuickRef'], resources_urls.get(dict_rep['QuickRef']))
    return dict_rep

def string_reconstruction(a, b=0, c=0):
    return f"{a:02d}.{b:02d}.{c:02d}"

def build_key_dict_list(listed_json):
    key_dict_list = {}
    for row in listed_json:
        ev_id = row['Ev_ID']
        a, b, c = map(int, ev_id.split('.'))
        data = row

        if string_reconstruction(a) not in key_dict_list:
            key_dict_list[ev_id] = {"value": data, "children": {}}
        else:
            if string_reconstruction(a, b) not in key_dict_list[string_reconstruction(a)]['children']:
                key_dict_list[string_reconstruction(a)]['children'][ev_id] = {"value": data, "children": {}}
            else:
                key_dict_list[string_reconstruction(a)]['children'][string_reconstruction(a, b)]['children'][ev_id] = {"value": data}

    return key_dict_list

def save_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def verify_tree_structure(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    count = 0
    for key_a, value_a in data.items():
        count += 1
        for key_b, value_b in data[key_a]['children'].items():
            count += 1
            for key_c, value_c in data[key_a]['children'][key_b]['children'].items():
                count += 1
    return count

def main():
    resources_urls = load_resources('The AI Risk Repository V1 - Included resources.csv')
    listed_json = process_risk_data('The AI Risk Repository V1 - AI Risk Database v1.csv', resources_urls)
    
    save_json(listed_json, "listed_representation.json")

    key_dict_list = build_key_dict_list(listed_json)
    save_json(key_dict_list, "mit_ai_risk_tree.json")

    verification_count = verify_tree_structure("mit_ai_risk_tree.json")
    assert len(listed_json) - 1 == verification_count
    print("Completed. mit_ai_risk_tree.json usable now!")

if __name__ == "__main__":
    main()