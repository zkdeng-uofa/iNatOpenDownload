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
  '--input_folder',
  type = str
)
parser.add_argument(
  '--data_dir',
   type = str
)
args = parser.parse_args()

# if not len(sys.argv) > 1:
#   while True:
#     try:
#       args.start_index = int(input('Enter a start index (i.e. 1): '))
#       break

#     except ValueError:
#       print("Incorrect Input")
#   print(f'Your start index is {args.start_index}\n')

#   while True:
#     try:
#       args.end_index = int(input('Enter an end index (i.e. 100): '))
#       break

#     except ValueError:
#       print("Incorrect Input")
#   print(f'Your end index is {args.end_index}\n')

#   while True:
#     try:
#       args.input_folder = input('Enter an input folder (i.e. insecta_csvs): ')
#       break

#     except ValueError:
#       print("Incorrect Input")
#   print(f'Your input folder is {args.input_folder}\n')

#   while True:
#     try:
#       args.data_dir = input('Enter a data directory (i.e. data): ')
#       break

#     except ValueError:
#       print("Incorrect Input")
#   print(f'Your data directory is {args.data_dir}\n')

os.makedirs(args.data_dir, exist_ok=True)
csv_list_path = f'{args.data_dir}/csv_list.csv'

def save_csv_list():
  if not os.path.exists(csv_list_path):
    csv_list = glob(f'csvs/{args.input_folder}/*.csv')

    df = pd.DataFrame(csv_list, columns=['csv_list'])
    df.csv_list = df.csv_list.map(lambda x: x.replace(f'csvs/{args.input_folder}/',''))
    df['downloaded'] = False

    df.to_csv(csv_list_path, index=True)

def update_csv_list(index_list: list):
  df_csv_list = pd.read_csv(csv_list_path, index_col=0)
  df_csv_list.loc[index_list, 'downloaded'] = True
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
  tar = tarfile.open(f'{os.path.abspath(args.data_dir)}/{tar_name}', "w:gz")

  index_list = list(range(args.start_index, args.end_index))

  try:
    index_check = df_csv_list.loc[index_list, 'csv_list']
  except:
    args.end_index = len(df_csv_list)
    index_list = list(range(args.start_index, args.end_index))
    #print(df_csv_list.loc[index_list, 'csv_list'])


  for i in tqdm(df_csv_list.loc[index_list, 'csv_list']):
    try:
      #print(index_list)
      csv_dir = f'csvs/{args.input_folder}/{i}'
      print(csv_dir)
      #csv_dir = f'{i}'
      df = pd.read_csv(csv_dir)

      output_folder = f'{args.data_dir}/{df.loc[0, "taxon_name"]}'

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
      tar.add(os.path.abspath(output_folder), arcname=df.loc[0, 'taxon_name'])


      # removing the previously not-compressed downloaded images

      parent_dir = df.loc[0,'taxon_name']
      shutil.rmtree(f'{args.data_dir}/{parent_dir}')

    except:
      index_list.pop(i)

  tar.close()

  update_csv_list(index_list)

  return tar_name

if __name__ == '__main__':
    tar_name = main(start_index=args.start_index, end_index=args.end_index, data_dir=args.data_dir)
