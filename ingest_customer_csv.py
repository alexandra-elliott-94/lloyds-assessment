import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import re
import json
from apache_beam.pvalue import TaggedOutput
from datetime import datetime
import jsonschema
from apache_beam.io.filesystems import FileSystems

def parse_schema(json_path: str):
    """Parse schema from a JSON file in GCS."""
    with FileSystems.open(f"gs://natural-pipe-469020-h2-dataflow-bucket/{json_path}") as f:
        print(f)
        schema = json.loads(f.read())
    return schema

class TransformData(beam.DoFn):
    """A helper class to transform CSV rows to BigQuery rows."""
    def __init__(self, schema):
        self.schema = schema

    def process(self, string_input):
        """Translates a line of comma separated values to a
        dictionary which can be loaded into BigQuery.

        Args:
            string_input: A comma separated list of values

        Returns:
            A dictionary where each key is a BigQuery column name and
              each value is the parsed result from string_input.
         """
      
        try:
            logging.info(f"Processing row: {string_input}")
            string_input = re.sub('"', '', string_input)
            string_input = re.sub('\r\n', '', string_input)
            values = re.split(",", string_input)
            
            columns = []
            for value in self.schema['properties']:
                columns.append(value)

            logging.info(columns)

            row = dict(
                zip(columns,
                    values))
            logging.info(f"Transformed row: {row}")

            for k, v in row.items():
                if not v:
                    if k in self.schema['required_fields']:
                        raise ValueError(f"Missing required field: {k}")
                    else:
                        v = None
                elif self.schema['properties'][k]['type'] == 'integer':
                    row[k] = int(v)
                elif self.schema['properties'][k]['type'] == 'string':
                    row[k] = str(v)
                else:
                    row[k] = v
            
            jsonschema.validate(instance=json.loads(json.dumps(row)), schema=self.schema)

            row['ingestion_timestamp'] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            yield TaggedOutput('valid', row)
        except Exception as e: 
            logging.error(f"Error parsing row: {string_input}, error: {e}")
            row = {'row': string_input, 'error': str(e), 'ingestion_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            yield TaggedOutput('invalid', row)



def run(argv=None):
    """Main entry point; defines and runs the pipeline."""
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

    schema = parse_schema(f"schemas/{known_args.table}/{known_args.table}.json")
    print(schema)

    p = beam.Pipeline(options=PipelineOptions(pipeline_args))


    valid, invalid = (p | 'Read from GCS' >> beam.io.ReadFromText(f"{known_args.source_file}",
                                                  skip_header_lines=1)
        | 'Transform to BigQuery Row' >> beam.ParDo(TransformData(schema)).with_outputs('valid', 'invalid'))
    
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



