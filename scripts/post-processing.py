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
from zipfile import ZipFile
import gzip


script_dir = Path(os.path.dirname(__file__))
logging.config.fileConfig(script_dir.parent / 'config' / 'logging.config')
logger = logging.getLogger('post-processing.py')


def compress_directory(input_path, output_path, tag):

    # Compress the whole directories:
    zip_path = Path(output_path, str(tag) + '.zip')

    with ZipFile(zip_path, 'w') as zip_file:
        for root, directories, files in os.walk(input_path):
            for filename in files:  
                file_path = Path(root, filename)
                relative_path = os.path.relpath(file_path, input_path)
                zip_file.write(file_path, arcname=relative_path)

    # Compress only the IRIDA Next JSON output file:
    zip_path = Path(output_path, str(tag) + '.iridanext.output.json.zip')
    gzip_path = Path(input_path, 'iridanext.output.json.gz')
    uncompressed_path = Path(input_path, 'iridanext.output.json')

    # Check if already GZIP-compressed:
    if gzip_path.exists():
        with gzip.open(gzip_path, 'r') as gzip_file, \
             ZipFile(zip_path, 'w') as zip_file:
            zip_file.writestr('iridanext.output.json', gzip_file.read())

    # Check if not compressed:
    elif uncompressed_path.exists():
        with ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(uncompressed_path, arcname='iridanext.output.json')

    # File isn't as expected:
    else:
        raise Exception("Could not find IRIDA Next JSON output file!")


def main():
    parser = argparse.ArgumentParser(prog='post-processing.py', description='Post-process gasnomenclature and arboratornf results')
    parser.add_argument('--gasnomenclature', action='store', dest='gasnomenclature', type=str, required=True)
    parser.add_argument('--arborator', action='store', dest='arborator', type=str, required=True)
    parser.add_argument('--output', action='store', dest='output', type=str, required=True)

    args = parser.parse_args()
    gasnomenclature_path = args.gasnomenclature
    arborator_path = args.arborator

    output_directory = Path(args.output)
    output_directory.mkdir(parents=True, exist_ok=True)

    gasnomenclature_tag = 'gasnomenclature'
    compress_directory(gasnomenclature_path, output_directory, gasnomenclature_tag)

    arborator_tag = 'arborator'
    compress_directory(arborator_path, output_directory, arborator_tag)


if __name__ == '__main__':
    main()