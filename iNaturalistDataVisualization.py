import sqlite3
import pandas as pd
import time
import os
import warnings
import plotly.express as px
import plotly.io as pio

def make_taxa_column(row, taxa_df, rank):
    ancestry_list = row.ancestry.split('/')
    for i in range(0, len(ancestry_list)):
        taxa = taxa_df.loc[taxa_df['taxon_id'] == int(ancestry_list[i])]
        if (taxa['rank'].values == rank):
            return taxa.name
        else:
            continue
    return 'No ' + rank

def make_species(row, taxa_df, sample_df, rank):
    if str(row['rank']) == rank:
        return row.taxon_name
    else:
        index = sample_df.index
        condition = sample_df['taxon_name'] == row.taxon_name
        indices = index[condition]
        indices_list = indices.tolist()

        #indicies_list = sample_df.index[sample_df['taxon_name'] == row.taxon_name].tolist()
        return  str(indices_list) + ' No ' + rank

def make_subspecies(row, taxa_df, rank):
    if str(row['rank']) == rank:
        return row.taxon_name
    else:
        return None

inat_con = sqlite3.connect("inaturalist-open-data-20220127.sq3db")
print(inat_con.total_changes)

insect_rank_count_df = pd.read_csv('iNaturalist_Insects_Rank_Count.csv')
#print(insect_rank_count_df.head())

sample_insect_rank_df = insect_rank_count_df[0:5000]

taxa_df = pd.read_sql(
    """
    SELECT name, taxon_id, ancestry, rank, rank_level
    FROM taxa
    """,
    inat_con
)

sample_insect_rank_df = pd.read_csv('iNaturalist_Insects_Taxa_Columns_T5000.csv')

warnings.filterwarnings('ignore')
pio.renderers.default = "browser"
#fig = px.sunburst(sample_insect_rank_df, path=['state_of_matter', 'kingdom', 'phylum', 'subphylum', 'class', 'subclass', 'order', 'superfamily', 'family', 'subfamily', 'tribe', 'genus', 'subgenus', 'taxon_name'], values='photo_count', color='photo_count')
fig = px.sunburst(sample_insect_rank_df, path=['class', 'subclass', 'order', 'superfamily', 'family', 'subfamily', 'tribe', 'genus', 'subgenus', 'species', 'subspecies'], values='photo_count',
                  color='photo_count', color_continuous_scale='Turbo')
                  #color_continuous_midpoint=np.average(sample_insect_rank_df['photo_count'], weights=sample_insect_rank_df['rank_level']))
fig.show()
