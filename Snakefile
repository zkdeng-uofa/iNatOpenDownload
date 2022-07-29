rule all:
  input:
    # "awscliv2.zip",
    "inaturalist-open-data-latest.tar.gz",
    "csvs/inat_meta_data"

rule download_meta_data:
  output:
    "inaturalist-open-data-latest.tar.gz"
  shell:
    "aws s3 cp s3://inaturalist-open-data/metadata/inaturalist-open-data-latest.tar.gz inaturalist-open-data-latest.tar.gz --no-sign-request"

# rule install_aws_linux:
#   output:
#     "awscliv2.zip"
#   shell:
#     """
#     curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#     unzip awscliv2.zip
#     sudo ./aws/install
#     """

rule extract_meta_data:
  input:
    "inaturalist-open-data-latest.tar.gz"
  output:
    directory("csvs/inat_meta_data")
  shell:
    """
    mkdir csvs/inat_meta_data
    tar -xvf inaturalist-open-data-latest.tar.gz -C csvs/inat_meta_data --strip-components 1
    """

# rule make_inat_db:
#   input:
#     "inat_meta_data"
#   output:
#     "db/inat_open_data.sq3db"
#   script:
#     "scripts/MakeiNatDB.py"

rule make_subset_url_db:
  input:
    "dbs/inaturalist-open-data-20220127.sq3db"
  output:
    "dbs/{subset}_db.sq3db"
  shell:
    """
    python scripts/SubsetOpenData.py
    """

rule create_subset_csv_files:
  input:
    "dbs/{subset}_db.sq3db"
  output:
    directory("csvs/{subset}_csvs")
  shell:
    """
    python scripts/MakeSubsetCsvs.py
    """

rule download_upload_imgs:
  input:
    "csvs/{subset}_csvs"
  output:
    directory("imgs/{subset}_imgs")
  shell:
    "bash scripts/DownloadUploadScript 1 5 {wildcards.subset}_csvs imgs/{wildcards.subset}_imgs"


