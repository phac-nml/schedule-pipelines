# schedule-pipelines

## GASNomenclature

```
nextflow run phac-nml/gasnomenclature -r 0.2.2 --input https://raw.githubusercontent.com/phac-nml/schedule-pipelines/refs/heads/main/test/data/samplesheet_gasnomeclasture.csv -w /tmp/gasnomenclature/work -profile docker -params-file https://raw.githubusercontent.com/phac-nml/schedule-pipelines/refs/heads/main/config/gasnomenclature-listeria.json -queue-size 4 --outdir /tmp/gasnomenclature/output
```

## Update Samplesheet

```
python scripts/update-samplesheet.py --json /tmp/gasnomenclature/output/iridanext.output.json.gz --samplesheet test/data/samplesheet_arborator.csv --output /tmp/updated_samplesheet.csv
```

## Arborator

```
nextflow run phac-nml/arboratornf -r 0.2.0 --input /tmp/updated_samplesheet.csv -w /tmp/arborator_detection/work -profile docker -params-file https://raw.githubusercontent.com/phac-nml/schedule-pipelines/refs/heads/main/config/arboratornf-detection-listeria.json -queue-size 4 --outdir /tmp/arborator_detection/output
```

## Post-Processing

```
python scripts/post-processing.py --gasnomenclature /tmp/gasnomenclature/output/ --arborator /tmp/arborator/output/ --output /tmp/post/
```

# Outputs

```
arborator_2024-10-03_13-42-34.iridanext.output.json.zip
arborator_2024-10-03_13-42-34.zip
gasnomenclature_2024-10-03_13-42-34.iridanext.output.json.zip
gasnomenclature_2024-10-03_13-42-34.zip
```

## Legal

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
