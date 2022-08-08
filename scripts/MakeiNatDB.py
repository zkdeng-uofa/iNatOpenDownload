import pandas as pd
import sqlite3
import os

con = sqlite3.connect("../db/inat_open_data.sq3db")
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

photos_df = pd.read_csv('../inat_meta_data/photos.csv', on_bad_lines='warn', delimiter="	")
photos_df.to_sql('photos', con, if_exists='replace', index=False)

taxa_df = pd.read_csv('../inat_meta_data/taxa.csv', on_bad_lines='warn', delimiter="	")
taxa_df.to_sql('taxa', con, if_exists='replace', index=False)

observers_df = pd.read_csv('../inat_meta_data/observers.csv', on_bad_lines='warn', delimiter="	")
observers_df.to_sql('observers', con, if_exists='replace', index=False)

observations_df = pd.read_csv('../inat_meta_data/observations.csv', on_bad_lines='warn', delimiter="	")
observations_df.to_sql('observations', con, if_exists='replace', index=False)

con.close()
