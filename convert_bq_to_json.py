import json
import glob

def get_bq_schemas():
    """ Get all BigQuery schema files in the schemas directory. """
    files = glob.glob('./schemas/*/*_bq.json')
    return files

def open_bq_schema(path):
    """ Open a BigQuery schema file and return its contents. """
    with open(path, 'r') as f:
        bq = f.read()
    return bq

def save_json_schema(path, schema):
    """ Save a JSON schema to a file. """
    with open(path, 'w') as f:
        json.dump(schema, f, indent=4)

def convert_bq_to_json(bq):
    """ Convert a BigQuery schema to a JSON schema. """
    json_schema = {}
    json_schema['type'] = 'object'
    json_schema['properties'] = {}
    json_schema['required_fields'] = []
    bq = json.loads(bq)
    for field in bq:
        if field['name'] != 'ingestion_timestamp':
            json_schema['properties'][field['name']] = {'type': field['type'].lower()}
            if field['mode'] == 'REQUIRED':
                json_schema['required_fields'].append(field['name'])
    return json_schema



if __name__ == '__main__':

    files = get_bq_schemas()
    for file in files:
        bq_schema = open_bq_schema(file)
        json_schema = convert_bq_to_json(bq_schema)
        filepath = file.split('_')[0]
        save_json_schema(f"{filepath}.json", json_schema)