rule all:
  input:
    "inaturalist-open-data-latest.tar.gz"

rule download_meta_data:
  output:
    "inaturalist-open-data-latest.tar.gz"
  shell:
    "aws s3 cp s3://inaturalist-open-data/metadata/inaturalist-open-data-latest.tar.gz inaturalist-open-data-latest.tar.gz --no-sign-request"
