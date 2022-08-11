import pandas as pd
import sqlite3
import os

con = sqlite3.connect("dbs/inat_open_data.sq3db")
cur = con.cursor()

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS observations (
        observation_uuid uuid NOT NULL,
        observer_id integer,
        latitude numeric(15,10),
        longitude numeric(15,10),
        positional_accuracy integer,
        taxon_id integer,
        quality_grade character varying(255),
        observed_on date
    );
    '''
)
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS photos (
        photo_uuid uuid NOT NULL,
        photo_id integer NOT NULL,
        observation_uuid uuid NOT NULL,
        observer_id integer,
        extension character varying(5),
        license character varying(255),
        width smallint,
        height smallint,
        position smallint
    );
    '''
)
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS taxa (
        taxon_id integer NOT NULL,
        ancestry character varying(255),
        rank_level double precision,
        rank character varying(255),
        name character varying(255),
        active boolean
    );
    '''
)
cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS observers (
        observer_id integer NOT NULL,
        login character varying(255),
        name character varying(255)
    );
    '''
)
con.commit()

photos_df = pd.read_csv('csvs/inat_meta_data/photos.csv', on_bad_lines='warn', delimiter="	")
photos_df.to_sql('photos', con, if_exists='replace', index=False)

taxa_df = pd.read_csv('csvs/inat_meta_data/taxa.csv', on_bad_lines='warn', delimiter="	")
taxa_df.to_sql('taxa', con, if_exists='replace', index=False)

observers_df = pd.read_csv('csvs/inat_meta_data/observers.csv', on_bad_lines='warn', delimiter="	")
observers_df.to_sql('observers', con, if_exists='replace', index=False)

observations_df = pd.read_csv('csvs/inat_meta_data/observations.csv', on_bad_lines='warn', delimiter="	")
observations_df.to_sql('observations', con, if_exists='replace', index=False)

cur.execute('CREATE UNIQUE INDEX "idx_observations_observation_uuid" ON "observations" ("observation_uuid")')
cur.execute('CREATE INDEX "idx_observations_observer_id" ON "observations" ("observer_id");')
cur.execute('CREATE INDEX "idx_observations_taxon_id" ON "observations" ("taxon_id")')
cur.execute('CREATE INDEX "idx_observations_quality_grade" ON "observations" ("quality_grade")')
cur.execute('CREATE INDEX "idx_observations_observed_on" ON "observations" ("observed_on")')
cur.execute('CREATE INDEX "idx_observations_longitude" ON "observations" ("longitude")')
cur.execute('CREATE INDEX "idx_observations_latitude" ON "observations" ("latitude")')

cur.execute('CREATE UNIQUE INDEX "idx_observers_login" ON "observers" ("login")')
cur.execute('CREATE UNIQUE INDEX "idx_observers_observer_id" ON "observers" ("observer_id")')

cur.execute('CREATE INDEX "idx_photos_photo_uuid" ON "photos" ("photo_uuid")')
cur.execute('CREATE INDEX "idx_photos_observation_uuid" ON "photos" ("observation_uuid")')
cur.execute('CREATE INDEX "idx_photos_photo_id" ON "photos" ("photo_id")')
cur.execute('CREATE INDEX "idx_photos_observer_id" ON "photos" ("observer_id")')
cur.execute('CREATE INDEX "idx_photos_license" ON "photos" ("license")')

cur.execute('CREATE UNIQUE INDEX "idx_taxa_taxon_id" ON "taxa" ("taxon_id")')
cur.execute('CREATE INDEX "idx_taxa_name" ON "taxa" ("name")')
cur.execute('CREATE INDEX "idx_taxa_rank" ON "taxa" ("rank")')
cur.execute('CREATE INDEX "idx_taxa_rank_level" ON "taxa" ("rank_level")')
cur.execute('CREATE INDEX "idx_taxa_ancestry" ON "taxa" ("ancestry")')

con.commit()

con.close()
