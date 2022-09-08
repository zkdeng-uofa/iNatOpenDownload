import argparse
import pandas as pd
import sqlite3
import os
#import pyinputplus as pyimp
import time
# import tqdm
# import art
import sys
#import dask.dataframe as dd

parser = argparse.ArgumentParser(
  description = 'Enter an ancestry to create a subset db'
)
parser.add_argument(
  '--taxon_name',
   type = str,
   help = 'The taxon name you want to subset'
)
parser.add_argument(
  '--ancestry_string',
   type = str,
   help = 'The ancestry string that is used in the SQL query'
)
parser.add_argument(
  '--csv_name',
   type = str,
   default = 'subset_data',
   help = 'Name of the csv'
)
parser.add_argument(
  '--input_db',
   type = str,
   default = 'inaturalist-open-data-20220127.sq3db',
   help = 'input database, iNaturalist Open Data'
)
parser.add_argument(
  '--output_db',
   type = str,
   default = 'idx_inaturalist_subset.sq3db',
   help = 'name of output database'
)
parser.add_argument(
  '--rank',
   type = str,
   default = 'species',
   help = 'name of species'
)
args = parser.parse_args()

if not len(sys.argv) > 1:
  while True:
    try:
      args.taxon_name = input('Enter a taxon name (i.e. Cigaritis): ')
      break

    except ValueError:
      print("Incorrect Input")
  print(f'Your taxon name is {args.taxon_name}\n')

  args.taxon_name = args.taxon_name
  args.csv_name = f'{args.taxon_name.replace(" ", "_")}'
  args.output_db = f'{args.taxon_name.replace(" ", "_")}_db.sq3db'

  # while True:
  #   try:
  #     args.input_db = input('Enter an input database: ')
  #     break

  #   except ValueError:
  #     print("Incorrect Input")
  # print(f'Your taxon name is {args.input_db}\n')

  while True:
    try:
      args.rank = input('Enter a rank (i.e. species): ')
      break

    except ValueError:
      print("Incorrect Input")
  print(f'Your input rank is {args.rank}\n')


taxon_df = pd.read_sql_query(
  "SELECT * "
  "FROM taxa "
  "WHERE name = '"+args.taxon_name+"' "
  "LIMIT 10 ",
  #con = "sqlite:///dbs/"+args.input_db
  con = "sqlite:///dbs/inat_open_data.sq3db"
)

args.ancestry_string = f'{taxon_df["ancestry"][0]}/%'

if (args.rank == "species"):
  url_df = pd.read_sql_query(
      "WITH urls AS (SELECT 'http://inaturalist-open-data.s3.amazonaws.com/photos/' AS photo_url) "
      "SELECT B.*, U.photo_url || A.photo_id || '/' || 'large.' || A.extension AS photo_url_large, D.name AS taxon_name, D.ancestry, D.taxon_id, D.rank, A.photo_id, A.photo_uuid, A.extension "
      "FROM urls U "
      "CROSS JOIN photos A "
      "JOIN observers B "
      "ON A.observer_id = B.observer_id "
      "JOIN observations C "
      "ON A.observation_uuid = C.observation_uuid "
      "LEFT JOIN taxa D "
      "ON C.taxon_id = D.taxon_id "
      "WHERE (D.ancestry LIKE '"+args.ancestry_string+"' AND C.quality_grade = 'research' AND D.rank = 'species') "
      "OR (D.ancestry LIKE '"+args.ancestry_string+"' AND C.quality_grade = 'research' AND D.rank = 'subspecies') ",
      #con = "sqlite:///dbs/"+args.input_db
      con = "sqlite:///dbs/inat_open_data.sq3db"
  )
else:
  url_df = pd.read_sql_query(
      "WITH urls AS (SELECT 'http://inaturalist-open-data.s3.amazonaws.com/photos/' AS photo_url) "
      "SELECT B.*, U.photo_url || A.photo_id || '/' || 'large.' || A.extension AS photo_url_large, D.name AS taxon_name, D.ancestry, D.taxon_id, D.rank, A.photo_id, A.photo_uuid, A.extension "
      "FROM urls U "
      "CROSS JOIN photos A "
      "JOIN observers B "
      "ON A.observer_id = B.observer_id "
      "JOIN observations C "
      "ON A.observation_uuid = C.observation_uuid "
      "LEFT JOIN taxa D "
      "ON C.taxon_id = D.taxon_id "
      "WHERE D.ancestry LIKE '"+args.ancestry_string+"' "
      "AND D.rank = '"+args.rank+"' "
      "AND C.quality_grade = 'research' ",
      #con = "sqlite:///dbs/"+args.input_db
      con = "sqlite:///dbs/inat_open_data.sq3db"
  )
url_df.to_csv('csvs/'+args.csv_name+'.csv', index=False)

print('CSV Created')

url_con = sqlite3.connect("dbs/"+args.output_db)
url_df.to_sql("subset", url_con, if_exists="replace")

cursor = url_con.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_ancestry" ON "subset" ("ancestry")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_login" ON "subset" ("login")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_name" ON "subset" ("name")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_observer_id" ON "subset" ("observer_id")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_photo_id" ON "subset" ("photo_id")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_photo_url_large" ON "subset" ("photo_url_large")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_photo_uuid" ON "subset" ("photo_uuid")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_subset_taxon_name" ON "subset" ("taxon_name")')
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS "idx_observations_index" ON "subset" ("index")')
cursor.execute('CREATE INDEX IF NOT EXISTS "ix_subset_index"ON "subset" ("index")')
url_con.commit()

