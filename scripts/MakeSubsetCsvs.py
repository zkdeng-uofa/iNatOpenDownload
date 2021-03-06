import argparse
import pandas as pd
import sqlite3
import os
#import pyinputplus as pyimp
import time
# import tqdm
# import art
import sys

parser = argparse.ArgumentParser(
  description = 'Enter a db to create csv folder'
)
parser.add_argument(
  '--input_db',
   type = str,
   help = 'input database to create csv files'
)
parser.add_argument(
  '--output_folder',
   type = str,
   default = 'subset_csvs',
   help = 'name of output folder'
)

args = parser.parse_args()

if not len(sys.argv) > 1:
  while True:
    try:
      args.input_db = input('Enter an input db (i.e. insect_species.sq3db): ')
      break

    except ValueError:
      print("Incorrect Input")
  print(f'Your input db is {args.input_db}\n')

  while True:
    try:
      args.output_folder = input('Enter an output folder (i.e. insect_species_csvs): ')
      break

    except ValueError:
      print("Incorrect Input")
  print(f'Your output folder is {args.output_folder}\n')

url_con = sqlite3.connect("dbs/"+args.input_db)

taxon_df = pd.read_sql_query(
    "SELECT DISTINCT taxon_name "
    "FROM subset ",
    url_con
)

os.makedirs("csvs/"+args.output_folder, exist_ok=True)
for i in range(0, len(taxon_df)):
    sql = """SELECT photo_url_large, taxon_name, ancestry, extension
             FROM subset
             WHERE taxon_name = ? """
    photo_df = pd.read_sql_query(sql, url_con, params=[taxon_df['taxon_name'][i]])

    if not os.path.exists('csvs/' + args.output_folder):
      os.mkdir('csvs/' + args.output_folder)
    taxon_name = taxon_df['taxon_name'][i].replace('/', ' ')
    path = 'csvs/' + args.output_folder + '/' + taxon_name + '.csv'

    #print(path)
    photo_df.to_csv(path, index=False)
