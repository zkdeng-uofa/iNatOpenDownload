import argparse
import pandas as pd
import sqlite3
import os
import time
# import tqdm
# import art
import sys
import yaml

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

url_con = sqlite3.connect(args.input_db)

taxon_df = pd.read_sql_query(
    "SELECT DISTINCT taxon_name, ancestry, rank "
    "FROM subset ",
    url_con
)

parent_taxa = taxon_df['ancestry'][0].split('/')[-1]

parent_taxa_df = pd.read_sql_query(
  "SELECT taxon_id, rank_level, rank, name "
  "FROM taxa "
  f"WHERE taxon_id = {parent_taxa}",
  con = "sqlite:///dbs/inat_open_data.sq3db"
)

print(parent_taxa_df)

# os.makedirs(args.output_folder, exist_ok=True)
# for i in range(0, len(taxon_df)):
#     sql = """SELECT photo_url_large, taxon_name, ancestry, extension
#              FROM subset
#              WHERE taxon_name = ? """
#     photo_df = pd.read_sql_query(sql, url_con, params=[taxon_df['taxon_name'][i]])

#     if not os.path.exists(args.output_folder):
#       os.mkdir(args.output_folder)
#     taxon_name = taxon_df['taxon_name'][i].replace('/', ' ')
#     path = args.output_folder + '/' + taxon_name.replace(" ", "_") + '.csv'

#     #print(path)
#     photo_df.to_csv(path, index=False)

os.makedirs(args.output_folder, exist_ok=True)
for i in range(0, len(taxon_df)):
    # sql = """SELECT photo_url_large, taxon_name, ancestry, extension
    #          FROM subset
    #          WHERE taxon_name = ? """
    sql = """SELECT *
             FROM subset
             WHERE taxon_name = ? """
    photo_df = pd.read_sql_query(sql, url_con, params=[taxon_df['taxon_name'][i]])

    taxon_name = taxon_df['taxon_name'][i].replace('/', ' ')
    path = args.output_folder + '/' + taxon_name.replace(" ", "_") + '.csv'

    #print(path)
    photo_df.to_csv(path, index=False)
    

taxon_name = args.output_folder
taxon_name = taxon_name[4:]
taxon_name = taxon_name[::-1]
taxon_name = taxon_name[5:]
taxon_name = taxon_name[::-1]

param_data = [
  {'taxon_name': taxon_name},
  {'start_index': 1},
  {'end_index': len(taxon_df)}
]

with open(f'yaml/{taxon_name}.yaml', 'w') as file:
    documents = yaml.dump(param_data, file)
  