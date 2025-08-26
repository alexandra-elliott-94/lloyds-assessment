import json
import glob

def get_bq_schemas():
    """ Get all BigQuery schema files in the schemas directory. """
    return glob.glob('./schemas/*/*_bq.json')

def open_bq_schema(path):
    """ Open a BigQuery schema file and return its contents. """
    with open(path, 'r', encoding='UTF-8') as f:
        bq = f.read()
    return bq

def save_json_schema(path, schema):
    """ Save a JSON schema to a file. """
    with open(path, 'w', encoding='UTF-8') as f:
        json.dump(schema, f, indent=4)

def convert_bq_to_json(bq):
    """ Convert a BigQuery schema to a JSON schema. """
    json_schema = {}
    json_schema['type'] = 'object'
    json_schema['properties'] = {}
    json_schema['required_fields'] = []
    bq = json.loads(bq)
    for field in bq:
        if field['mode'] == 'REQUIRED':
            json_schema['required_fields'].append(field['name'])
        if field['type'] == 'DATETIME':
            json_schema['properties'][field['name']] = {'type': 'string'}
        elif field['type'] == 'NUMERIC':
            json_schema['properties'][field['name']] = {'type': 'number'}
        else:
            json_schema['properties'][field['name']] = {'type': field['type'].lower()}

    return json_schema



if __name__ == '__main__':

    files = get_bq_schemas()
    for file in files:
        bq_schema = open_bq_schema(file)
        new_json_schema = convert_bq_to_json(bq_schema)
        filepath = file.split('_')[0]
        save_json_schema(f"{filepath}.json", new_json_schema)
