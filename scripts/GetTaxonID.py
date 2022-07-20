import argparse
import pandas as pd
import sqlite3
import os
import time
import sys

parser = argparse.ArgumentParser(
  description = 'Enter an taxon name'
)
parser.add_argument(
  '--taxon_name',
   type = str,
   help = 'The taxon_name you want a taxon_id for'
)

args = parser.parse_args()

if not len(sys.argv) > 1:
  while True:
    try:
      args.taxon_name = input('Enter an taxon_name (i.e. insecta): ')
      break

    except ValueError:
      print("Incorrect Input")
  print(f'Your taxon name input is {args.taxon_name}\n')

# taxon_df = pd.read_sql_query(
#     "WITH urls AS (SELECT 'http://inaturalist-open-data.s3.amazonaws.com/photos/' AS photo_url) "
#     "SELECT B.*, U.photo_url || A.photo_id || '/' || 'large.' || A.extension AS photo_url_large, D.name AS taxon_name, D.ancestry, D.taxon_id, A.photo_id, A.photo_uuid, A.extension "
#     "FROM urls U "
#     "CROSS JOIN photos A "
#     "JOIN observers B "
#     "ON A.observer_id = B.observer_id "
#     "JOIN observations C "
#     "ON A.observation_uuid = C.observation_uuid "
#     "LEFT JOIN taxa D "
#     "ON C.taxon_id = D.taxon_id "
#     "WHERE D.ancestry LIKE '"+args.ancestry_string+"' "
#     "AND D.rank = '"+args.rank+"' "
#     "AND C.quality_grade = 'research' ",
#     #con = 'sqlite:///../db/inaturalist-open-data-20220127.sq3db'
#     #con = "sqlite:///../dbs/"+args.input_db
#     con = "sqlite:///dbs/"+args.input_db
# )

taxon_df = pd.read_sql_query(
  "SELECT * "
  "FROM taxa "
  "WHERE name = '"+args.taxon_name+"' "
  "LIMIT 10 ",
  con =  "sqlite:///dbs/inaturalist-open-data-20220127.sq3db"
)

print(taxon_df)
