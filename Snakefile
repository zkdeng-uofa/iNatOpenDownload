import os
import pandas as pd

#################### --- Default Rules --- ####################

rule all:
  input:
    # "awscliv2.zip",
    "inaturalist-open-data-latest.tar.gz",
    "csvs/inat_meta_data",
    "dbs/inat_open_data.sq3db"

#################### --- Functions --- ####################

def get_all_csvs(wildcards):
  folder_list = []
  path = f'csvs/Imgs-{wildcards.subset}_csvs/'
  for i in os.listdir(path):
    if i.endswith(".csv"):
      taxon_name = i[::-1]
      taxon_name = taxon_name[4:]
      taxon_name = taxon_name[::-1]
      folder_path = f'imgs/Imgs-{wildcards.subset}/{taxon_name}'
      folder_list.append(folder_path.replace(" ", "_"))
  return folder_list 

def get_range_csvs(wildcards):
  folder_list = []
  path = f'csvs/Imgs-{wildcards.subset}_csvs/'
  for i, val in enumerate(os.listdir(path)):
    if (i-1 >= int(wildcards.min)) & (i-1 <= int(wildcards.max)):
      if val.endswith(".csv"):
        taxon_name = val[::-1]
        taxon_name = taxon_name[4:]
        taxon_name = taxon_name[::-1]
        folder_path = f'imgs/Imgs-{wildcards.subset}_{wildcards.min}-{wildcards.max}/{taxon_name}'
        folder_list.append(folder_path.replace(" ", "_"))
  return folder_list 

########## --- iNaturalist Open Data DB Creation Rules --- ##########
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
    mkdir {output}
    tar -xvf {input} -C csvs/inat_meta_data --strip-components 1
    """

rule make_inat_db:
  input:
    "csvs/inat_meta_data"
  output:
    "dbs/inat_open_data.sq3db"
  script:
    "scripts/MakeiNatDB.py"

#################### --- DB Creation Rules --- ####################

rule make_subset_url_db:
  input:
    "dbs/inat_open_data.sq3db"
  output:
    "dbs/Imgs-{subset}_db.sq3db"
  shell:
    """
    python scripts/SubsetOpenData.py
    """

#################### --- CSV Creation Rules --- ####################

rule create_subset_csv_files:
  input:
    "dbs/Imgs-{subset}_db.sq3db"
  output:
    directory("csvs/Imgs-{subset}_csvs")
  shell:
    "python scripts/MakeSubsetCsvs.py --input_db {input} --output_folder {output}"

rule create_new_imgs_csvs:
  input:
    "dbs/Updated-{query}.sq3db"
  output:
    directory("csvs/Updated-{query}_csvs")
  shell:
    "python scripts/MakeSubsetCsvs.py --input_db {input} --output_folder {output}"

#################### --- Image Download Rules --- ####################

rule all_species_download:
  input:
    "csvs/Imgs-{subset}_csvs",
  output:
    directory("imgs/Imgs-{subset}/{species}")
  shell:
    "python scripts/SpeciesImgDownload.py" 
    " --input_folder {input}"
    " --input_csv {input}/{wildcards.species}.csv"
    " --data_dir imgs/Imgs-{wildcards.subset}"

rule download_imgs_all:
  input:
    get_all_csvs
  output:
    "yaml/Imgs-{subset}.yaml"
  run:
    for i in input:
      if (len(os.listdir(i)) == 1):
        os.system(f'rm -r {i}')
    os.system(f"echo 'Download Complete' > {output}")

rule range_species_download:
  input:
    "csvs/{subset}_csvs",
  output:
    directory("imgs/{subset}_{min}-{max}/{species}")
  wildcard_constraints:
    min = "\d+",
    max = "\d+"
  shell:
    "python scripts/SpeciesImgDownload.py"
    " --input_folder {input}"
    " --input_csv {input}/{wildcards.species}.csv"
    " --data_dir imgs/{wildcards.subset}_{wildcards.min}-{wildcards.max}"

rule download_upload_imgs_range:
  input:
    get_range_csvs
  output:
    "yaml/{subset}_{min}-{max}.yaml"
  wildcard_constraints:
    min = "\d+",
    max = "\d+"
  run:
    for i in input:
      if (len(os.listdir(i)) == 1):
        os.system(f'rm -r {i}')
    os.system(f"echo 'Download Complete' > {output}")

#################### --- Compression Rules --- ####################

rule compress_imgs:
  input:
    "yaml/{img_folder}.yaml"
  output:
    "tar_files/{img_folder}/{img_folder}.tar.gz"
  shell:
    "python scripts/TarImgs.py"
    " --img_folder {wildcards.img_folder}"

#################### --- Cyverse Rules --- ####################

rule cyverse_csv_upload:
  input:
    "csvs/{subset}_csvs"
  output:
    "yaml/{subset}_upload.yaml"
  shell:
    """
    echo 'Upload Complete' > {output}
    iput -rfPT {input} /iplant/home/shared/soynomics/inaturalist/iNatOpenDownload/{wildcards.subset}_csvs
    """

rule cyverse_csv_download:
  output:
    "yaml/{subset}_cyverse_download.yaml"
  shell:
    """
    echo "Download Complete" > {output}
    iget -rfPT /iplant/home/shared/soynomics/inaturalist/iNatOpenDownload/{wildcards.subset}_csvs csvs/{wildcards.subset}_csvs
    """

#################### --- Test Rules --- ####################

rule clean:
  shell:
    """
    rm -rfv csvs/*_csvs
    rm -rfv dbs/*_db.sq3db
    rm -rfv imgs/*_all-imgs
    rm -rfv yaml/_all-imgs.yaml
    """