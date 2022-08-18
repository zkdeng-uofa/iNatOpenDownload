import os

rule all:
  input:
    # "awscliv2.zip",
    "inaturalist-open-data-latest.tar.gz",
    "csvs/inat_meta_data",
    "dbs/inat_open_data.sq3db"

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

rule make_inat_db:
  input:
    "csvs/inat_meta_data"
  output:
    "dbs/inat_open_data.sq3db"
  script:
    "scripts/MakeiNatDB.py"

rule make_subset_url_db:
  input:
    "dbs/inat_open_data.sq3db"
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
    "python scripts/MakeSubsetCsvs.py --input_db {wildcards.subset}_db.sq3db --output_folder {wildcards.subset}_csvs"


rule download_upload_imgs_range:
  input:
    "csvs/{subset}_csvs"
  output:
    directory("imgs/{subset}_{min}_{max}_imgs")
  shell:
    "bash scripts/DownloadUploadScript -s {wildcards.min} -e {wildcards.max} -i csvs/{wildcards.subset}_csvs -o imgs/{wildcards.subset}_{wildcards.min}_{wildcards.max}_imgs"

rule download_upload_imgs_all:
  input:
    "csvs/{subset}_csvs"
  output:
    directory("imgs/{subset}_all-imgs")

  shell:
    "bash scripts/DownloadUploadScript -i csvs/{wildcards.subset}_csvs -o imgs/{wildcards.subset}_all-imgs -a true"

# for i in range(1, 10):
#   rule:
#     input: "dbs/inat_open_data.sq3db"
#     output: f"yaml/test_folder_{i}"
#     params: len = i
#     shell: "python scripts/yaml_test.py --input {wildcards.i}"

# rule:
#   input: 
#   output: "stats.yaml"

# rule download_stats:
#   input: "stats.yaml"

# def get_all_csvs(wildcards):
#   csv_list = []
#   path = 'csvs/Megapis_csvs/'
#   for i in os.listdir(path):
#     if i.endswith(".csv"):
#       csv_list.append(path + i)
#   return csv_list

def get_all_csvs(wildcards):
  folder_list = []
  path = f'csvs/{wildcards.subset}_csvs/'
  for i in os.listdir(path):
    if i.endswith(".csv"):
      taxon_name = i[::-1]
      taxon_name = taxon_name[4:]
      taxon_name = taxon_name[::-1]
      folder_path = f'imgs/{wildcards.subset}_all-imgs/{taxon_name}'
      folder_list.append(folder_path.replace(" ", "_"))
      # taxon_name = taxon_name[::-1]
  return folder_list
# taxon_name = taxon_name[5:]

rule multi_download_test:
  input:
    "csvs/{subset}_csvs"
  output:
    directory("imgs/{subset}_all-imgs/{species}")
  
  shell:
    "python scripts/SpeciesImgDownload.py --input_folder csvs/{wildcards.subset}_csvs --input_csv csvs/{wildcards.subset}_csvs/{wildcards.species}.csv --data_dir imgs/{wildcards.subset}_all-imgs"

  # shell:
  #   "mkdir imgs/Megapis_all-imgs/{wildcards.species}"

rule aggregate_test:
  input:
    get_all_csvs
  output:
    directory("imgs/{subset}_agg_imgs")
  shell: 
    "mkdir imgs/{wildcards.subset}_agg_imgs"
