import pandas as pd
import re
import json

def get_tactic_json(tactic_name, final_json):
    if tactic_name in final_json:
        return final_json[tactic_name]
    else:
        return json.dumps({"error": f"No data found for tactic '{tactic_name}'"})
    
def get_technique_json(technique_name, final_json):
    tactic_found = []
    sub_techniques = []

    for tactic, techniques in final_json.items():
        if technique_name in techniques:
            tactic_found.append(tactic)
            sub_techniques = techniques[technique_name].get('sub-techniques', [])

    if tactic_found:
        response = {
            "Technique": technique_name,
            "Tactics": tactic_found,
            "Sub-techniques": sub_techniques
        }
        return response
    else:
        return json.dumps({"error": f"No data found for technique '{technique_name}'"})

def clean_and_split_text(text):
    cleaned_text = text.replace('= ', '')

    separated_text = re.split(r'\s\s+', cleaned_text)

    cleaned_groups = [re.sub(r'\s*\(\d+\)\s*', '', part).strip() for part in separated_text]

    return cleaned_groups

def scrape():
    techniques = pd.read_html('https://attack.mitre.org/techniques/enterprise/')
    tech_df = techniques[0]

    techniques_dict = {}

    current_technique = None

    for index, row in tech_df.iterrows():
        if not pd.isna(row['ID']):
            current_technique = row['Name']
            techniques_dict[current_technique] = {'sub-techniques': []}
        else:
            if current_technique is not None:
                techniques_dict[current_technique]['sub-techniques'].append(row['Name'])

    matrice = pd.read_html('https://attack.mitre.org/matrices/enterprise/#')

    df = matrice[0]

    multi_index_data = df.columns

    tactics_dict = {}

    for key, value in multi_index_data:
        tactic_name = key  
        num_techniques = int(value.split()[0]) 

        tactics_dict[tactic_name] = num_techniques

    tacts = []
    for key in tactics_dict.keys():
        tacts.append(key)
    
    result = {}

    for i in range(len(tacts)):
        chunk = df.iloc[0][i]
        cleaned_text = clean_and_split_text(chunk)

        result[tacts[i]] = {'techniques': []}

        for technique in techniques_dict.keys():
            if technique in cleaned_text:
                result[tacts[i]]['techniques'].append(technique)

    final_json = {}

    for tactic, info in result.items():
        techniques = info['techniques']
        final_json[tactic] = {}
        for technique in techniques:
            final_json[tactic][technique] = {
                'sub-techniques': techniques_dict.get(technique, {}).get('sub-techniques', [])
            }

    return final_json

