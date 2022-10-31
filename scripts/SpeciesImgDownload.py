from asyncio import subprocess
import img2dataset
import pandas as pd
from glob import glob
from tqdm import tqdm
import tarfile
import argparse
import os
import shutil
import sys

parser = argparse.ArgumentParser('Input CSV Files')
parser.add_argument(
    '--input_folder',
    type = str
)
parser.add_argument(
    '--input_csv',
    type = str
)
parser.add_argument(
    '--data_dir',
    type = str
)
args = parser.parse_args()

def main():
    df = pd.read_csv(args.input_csv)

    if (df["rank"][0] == "subspecies"):
        parent_taxa = df['ancestry'][0].split('/')[-1]

        parent_taxa_df = pd.read_sql_query(
            "SELECT taxon_id, rank_level, rank, name "
            "FROM taxa "
            f"WHERE taxon_id = {parent_taxa}",
            con = "sqlite:///dbs/inat_open_data.sq3db"
        )

        os.makedirs(f'{args.data_dir}/{df.loc[0, "taxon_name"].replace(" ", "_")}', exist_ok=True)
        output_folder = f'{args.data_dir}/{parent_taxa_df["name"][0].replace(" ", "_")}/{df.loc[0, "taxon_name"].replace(" ", "_")}'

        try: 
            img2dataset.download(
                processes_count=1,
                thread_count=64,
                url_list=args.input_csv,
                output_folder=output_folder,
                output_format='webdataset',
                input_format='csv',
                url_col='photo_url_large',
                number_sample_per_shard=1000000,
                distributor='multiprocessing',
                resize_mode='no'
            )
        except:
            None
    else:
        output_folder = f'{args.data_dir}/{df.loc[0, "taxon_name"].replace(" ", "_")}'
        try: 
            img2dataset.download(
                processes_count=1,
                thread_count=64,
                url_list=args.input_csv,
                output_folder=output_folder,
                output_format='webdataset',
                input_format='csv',
                url_col='photo_url_large',
                number_sample_per_shard=1000000,
                distributor='multiprocessing',
                resize_mode='no'
            )
        except:
            None

if __name__ == '__main__':
    main()