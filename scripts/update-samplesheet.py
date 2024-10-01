#!/usr/bin/env python
"""
Copyright Government of Canada 2024

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

-------------------------------------------------------------------------------
"""
import argparse

import os
import logging
import logging.config
from pathlib import Path
import json
import gzip

script_dir = Path(os.path.dirname(__file__))
logging.config.fileConfig(script_dir.parent / 'config' / 'logging.config')
logger = logging.getLogger('run-pipelines.py')


def parse_addresses(json_path):

    open_function = gzip.open if str(json_path).endswith(".gz") else open

    with open_function(json_path, 'r') as file:
        data = json.load(file)

    addresses = {}

    for sample in data["metadata"]["samples"]:
        addresses[sample] = data["metadata"]["samples"][sample]["address"]

    return addresses


def update_addresses(samplesheet_path, addresses):

    updated_path = "/tmp/samplesheet.updated.csv"

    with open(samplesheet_path, 'r') as input_file, \
        open(updated_path, 'w') as output_file:

        # Header
        header = input_file.readline()
        output_file.write(header)

        # Rows
        for line in input_file:
            tokens = line.split(",")

            sample = tokens[0]
            if sample in addresses:
                tokens[2] = addresses[sample]

            output_file.write(",".join(tokens))

    return updated_path


def main():
    parser = argparse.ArgumentParser(prog='update-samplesheet.py', description='Update an arboratornf sample sheet with gasnomenclature results')
    parser.add_argument('--json', action='store', dest='json', type=str, required=True)
    parser.add_argument('--samplesheet', action='store', dest='samplesheet', type=str, required=True)

    args = parser.parse_args()
    json_path = args.json
    samplesheet_path = args.samplesheet

    addresses = parse_addresses(json_path)
    updated_samplesheet_path = update_addresses(samplesheet_path, addresses)


if __name__ == '__main__':
    main()