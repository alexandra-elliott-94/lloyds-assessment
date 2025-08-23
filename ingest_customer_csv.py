import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import re
import json
from apache_beam.pvalue import TaggedOutput
from datetime import datetime
import jsonschema

class TransformData(beam.DoFn):
    """A helper class which contains the logic to translate the file into
    a format BigQuery will accept."""

    def process(self, string_input):



        schema = {
                    "type": "object",
                    "properties": {
                        "first_name": {
                            "type": "string"
                        },
                        "last_name": {
                            "type": "string"
                        },
                        "phone_number": {
                            "type": "string"
                        },
                        "email": {
                            "type": "string"
                        },
                        "address": {
                            "type": "string"
                        },
                        "post_code": {
                            "type": "string"
                        },
                        "country": {
                            "type": "string"
                        },
                        "customer_id": {
                            "type": "integer"
                        }
                    },
                    "required_fields": [
                        "first_name",
                        "last_name",
                        "email",
                        "address",
                        "country",
                        "customer_id"
                    ]
        }

        try:
            logging.info(f"Processing row: {string_input}")
            string_input = re.sub('"', '', string_input)
            string_input = re.sub('\r\n', '', string_input)
            values = re.split(",", string_input)
            
            columns = []
            for value in schema['properties']:
                columns.append(value)

            logging.info(columns)

            row = dict(
                zip(columns,
                    values))
            logging.info(f"Transformed row: {row}")

            for k, v in row.items():
                if not v:
                    if k in schema['required_fields']:
                        raise ValueError(f"Missing required field: {k}")
                    else:
                        v = None
                elif schema['properties'][k]['type'] == 'integer':
                    row[k] = int(v)
                elif schema['properties'][k]['type'] == 'string':
                    row[k] = str(v)
                else:
                    row[k] = v
            
            jsonschema.validate(instance=json.loads(json.dumps(row)), schema=schema)

            row['ingestion_timestamp'] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            yield TaggedOutput('valid', row)
        except Exception as e: 
            logging.error(f"Error parsing row: {string_input}, error: {e}")
            row = {'row': string_input, 'error': str(e), 'ingestion_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            yield TaggedOutput('invalid', row)



def run(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset',
                        dest='dataset',
                        required=True,
                        help='Output BQ dataset to write results to.',
                        default='data_landing')
    parser.add_argument('--table',
                        dest='table',
                        required=True,
                        help='Output BQ table to write results to.',
                        default='data_landing.customers')
    parser.add_argument('--source_file',
                        dest='source_file',
                        required=True,
                        help='Path to the source file in GCS.',
                        default='gs://natural-pipe-469020-h2-data-landing/customers.csv')

    known_args, pipeline_args = parser.parse_known_args(argv)

    p = beam.Pipeline(options=PipelineOptions(pipeline_args))

    valid, invalid = (p | 'Read from GCS' >> beam.io.ReadFromText(f"{known_args.source_file}",
                                                  skip_header_lines=1)
        | 'Transform to BigQuery Row' >> beam.ParDo(TransformData()).with_outputs('valid', 'invalid'))
    
    valid    | 'Write to valid rows to BigQuery' >> beam.io.WriteToBigQuery( 
                f"natural-pipe-469020-h2:{known_args.dataset}.{known_args.table}",
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )

    invalid | 'Write to invalid rows to BigQuery' >> beam.io.WriteToBigQuery(
            f"natural-pipe-469020-h2:invalid_{known_args.dataset}.{known_args.table}",
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
    )

    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    run()



