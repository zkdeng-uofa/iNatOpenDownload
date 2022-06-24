import argparse
import pandas as pd
import sqlite3
import os
#import dask.dataframe as dd

parser = argparse.ArgumentParser(
  description = 'Enter an ancestry to create a subset db'
)
parser.add_argument(
  '--ancestry_string',
   type = str,
   required = True,
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
  '--output_folder',
   type = str,
   default = 'subset_csvs',
   help = 'name of output folder'
)
args = parser.parse_args()

url_df = pd.read_sql_query(
    "WITH urls AS (SELECT 'http://inaturalist-open-data.s3.amazonaws.com/photos/' AS photo_url) "
    "SELECT B.*, U.photo_url || A.photo_id || '/' || 'large.' || A.extension AS photo_url_large, D.name AS taxon_name, D.ancestry, D.taxon_id, A.photo_id, A.photo_uuid, A.extension "
    "FROM urls U "
    "CROSS JOIN photos A "
    "JOIN observers B "
    "ON A.observer_id = B.observer_id "
    "JOIN observations C "
    "ON A.observation_uuid = C.observation_uuid "
    "LEFT JOIN taxa D "
    "ON C.taxon_id = D.taxon_id "
    "WHERE D.ancestry LIKE '"+args.ancestry_string+"' "
    "AND D.rank = 'species' "
    "AND C.quality_grade = 'research' ",
    #con = 'sqlite:///../db/inaturalist-open-data-20220127.sq3db'
    con = "sqlite:///../db/"+args.input_db
)

url_df.to_csv('../csvs/'+args.csv_name+'.csv', index=False)

print('CSV Created')

#url_con = sqlite3.connect("../db/idx_inaturalist_subset.sq3db")
url_con = sqlite3.connect("../db/"+args.output_db)
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

#url_con = sqlite3.connect("../db/idx_inaturalist_subset2.sq3db")

taxon_df = pd.read_sql_query(
    "SELECT DISTINCT taxon_name "
    "FROM subset ",
    url_con
)

os.makedirs("../csvs/"+args.output_folder, exist_ok=True)
for i in range(0, len(taxon_df)):
    sql = """SELECT photo_url_large, taxon_name, ancestry, extension
             FROM subset
             WHERE taxon_name = ? """
    photo_df = pd.read_sql_query(sql, url_con, params=[taxon_df['taxon_name'][i]])

    #path = 'Species_CSVs/' + taxon_df['taxon_name'][i] + '.csv'
    path = args.output_folder + '/' + taxon_df['taxon_name'][i] + '.csv'
    photo_df.to_csv(path, index=False)

