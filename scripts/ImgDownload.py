from asyncio import subprocess
import img2dataset
import pandas as pd
from glob import glob
from tqdm import tqdm
import tarfile
import argparse
import os
import shutil

""" Example: python3 download.py --start_index 0 --end_index 10 --data_dir ../data/ --force_rewrite_csv_list 0 """

parser = argparse.ArgumentParser('Input which imgs from csv files to download')
parser.add_argument(
  '--start_index',
   type = int,
   default = 1
)
parser.add_argument(
  '--end_index',
   type = int,
   default = 100
)
parser.add_argument(
  '--data_dir',
   type = int
)
args = parser.parse_args()

csv_list_path = f'{args.data_dir}/csv_list.csv'

def save_csv_list():
  if not os.path.exists(csv_list_path):
    csv_list = glob(f'{args.data_dir}/species_csv/*.csv')

    df = pd.Dataframe(csv_list, columns=['csv_list'])
    df.csv_list = df.csv_list.map(lambda x: x.replace(f'{args.data_dir}/species_csv/',''))
    df['downloaded'] = False

    df.to_csv(csv_list_path, index=True)

def update_csv_list(index_list, list):
  df_csv_list = pd.read_csv(csv_list_path, index_col=0)
  cf_csv_list.loc[index_list, 'downloaded'] = True
  df_csv_list.to_csv(csv_list_path, index=True)

def checking_conditions(number_of_csvs=0):
    """ checking the conditions for downloading the images """

    assert args.end_index < number_of_csvs, f'end index is greater than the number of csvs: {number_of_csvs}'
    assert args.start_index < args.end_index, 'start index can not be greater than end index'
    assert args.start_index >= 0, 'start index can not be negative'
    assert args.end_index >= 0  , 'end index can not be negative'

def main(start_index=0, end_index=10, data_dir=''):
  save_csv_list()
  df_csv_list = pd.read_csv(csv_list_path, index_col=0)

  tar_name = f'{args.start_index}_{args.end_index}.tar.gz'
  tar = tarfile.open(f'os.path')

  index_list = list(range(args.start_index, args.end_index+1))

  for i in tqdm(df_csv_list.loc(index_list, 'csv_list')):
    try:
      csv_dir = f'{args.data_dir}/species_csv/{i}'
      df = pd.read_csv(csv_dir)

      output_folder = f'{args.data_dir}/{df.loc[0, "ancestry"]}'
              img2dataset.download(processes_count=16,
                                  thread_count=32,
                                  url_list=csv_dir,
                                  output_folder=output_folder,
                                  output_format='webdataset',
                                  input_format='csv',
                                  url_col='photo_url_large',
                                  number_sample_per_shard=200000,
                                  distributor='multiprocessing',
                                  resize_mode='no')
      tar.add(os.path.abspath(output_folder), arcname=df.loc[0,'ancestry'])


        # removing the previously not-compressed downloaded images
        parent_dir = df.loc[0,'ancestry'].split('/')[0]
        shutil.rmtree(f'{args.data_dir}/{parent_dir}')

    except:
        index_list.pop(i)

    tar.close()

    update_csv_list(index_list)

    return tar_name

if __name__ == '__main__':
    tar_name = main(start_index=args.start_index, end_index=args.end_index, data_dir=args.data_dir, force_rewrite_csv_list=args.force_rewrite_csv_list)
