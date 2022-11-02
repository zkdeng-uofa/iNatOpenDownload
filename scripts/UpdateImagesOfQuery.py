import pandas as pd
import sqlite3
import os
import argparse
import time
import sys

parser = argparse.ArgumentParser(
    description = 'Enter two query csvs'
)
parser.add_argument(
    '--outdated_csv',
    type = str,
    help = 'Previous CSV file'
)
parser.add_argument(
    '--updated_csv',
    type = str,
    help = 'New CSV File'
)
parser.add_argument(
    '--query_name',
    type = str,
    help = 'Name of query'
)
args = parser.parse_args()

if not len(sys.argv) > 1:
    while True:
        try:
            args.query_name = input('Enter query name: ')
            break

        except ValueError:
            print("Incorrect Input")
    print(f'Your query name is {args.query_name}')

    while True:
        try:
            args.outdated_csv = input('Enter outdated CSV: ')
            break

        except ValueError:
            print("Incorrect Input")
    print(f'Your outdated csv is {args.outdated_csv}')

    while True:
        try:
            args.updated_csv = input('Enter updated CSV: ')
            break

        except ValueError:
            print("Incorrect Input")
    print(f'Your updated csv is {args.updated_csv}')


outdated_df = pd.read_csv(f'csvs/{args.outdated_csv}')
updated_df = pd.read_csv(f'csvs/{args.updated_csv}')

merged_df = updated_df.merge(
    outdated_df.drop_duplicates(), 
    on = ['photo_id'],
    how = 'left',
    indicator = True,
    suffixes = ["", "_right"]
    )

new_imgs_df = merged_df[merged_df['_merge'] == 'left_only']
new_imgs_df.to_csv(f'csvs/Updated-{args.query_name}.csv', index=False)

#print(new_imgs_df)

new_imgs_con = sqlite3.connect(f'dbs/Update-{args.query_name}_db.sq3db')
new_imgs_df.to_sql("subset", new_imgs_con, if_exists="replace")

cursor = new_imgs_con.cursor()
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_ancestry" ON "subset" ("ancestry")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_login" ON "subset" ("login")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_name" ON "subset" ("name")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_observer_id" ON "subset" ("observer_id")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_photo_id" ON "subset" ("photo_id")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_photo_url_large" ON "subset" ("photo_url_large")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_photo_uuid" ON "subset" ("photo_uuid")')
cursor.execute('CREATE INDEX IF NOT EXISTS "idx_taxon_name" ON "subset" ("taxon_name")')
cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS "idx_observations_index" ON "subset" ("index")')
cursor.execute('CREATE INDEX IF NOT EXISTS "ix_index"ON "subset" ("index")')
new_imgs_con.commit()
