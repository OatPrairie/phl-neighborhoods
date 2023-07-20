import pandas as pd

from census_api.census_data import get_census_block_data
from census_api.constants import COLUMN_MAPPING, GROUPS


def convert_to_df(data: list) -> pd.DataFrame:
    """
    Convert data from Census API to a pandas dataframe and convert geographic hierarchy
    to the geo_id used to map blocks to neighborhoods
    """
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    cols = ['state', 'county', 'tract', 'block']
    df['geo_id'] = df[cols].apply(lambda row: ''.join(row), axis=1)
    df = df.drop(cols, axis=1)

    return df

def download_census_block_data() -> None:
    '''
    Retrieve block data from Census API, generate geo_id, and save as a csv file
    for mapping to neighborhoods
    '''
    census_block_data = get_census_block_data()
    census_block_df = convert_to_df(census_block_data)
    census_block_df.to_csv('data_sets/census_block_data.csv', index=False)

    return

def get_neighborhood_demographics(census_df: pd.DataFrame) -> pd.DataFrame:
    '''
    Map Census block geo_id values to neighboorhoodss and aggregate their population demographics
    '''
    mapping_df = pd.read_csv('data_sets/block_neighborhood_mapping.csv')
    census_df = census_df.astype('int')
    neighborhoods_df = census_df.merge(mapping_df, on='geo_id', how='left')
    neighborhoods_df = neighborhoods_df.drop('geo_id', axis=1)
    neighborhoods_df = neighborhoods_df.rename(columns=COLUMN_MAPPING)
    neighborhoods_df['median_age_product'] = neighborhoods_df['total_population'] * neighborhoods_df['median_age']
    neighborhoods_df = neighborhoods_df.drop('median_age', axis=1)
    neighborhoods_df = neighborhoods_df.groupby(['name']).sum()
    neighborhoods_df['mean_of_median_age'] = (
        neighborhoods_df['median_age_product'] / neighborhoods_df['total_population']
    ).round(1)  

    for group in GROUPS:
        group_col = neighborhoods_df.columns[neighborhoods_df.columns.str.endswith(group)][0]
        percentage_column = 'adult_percentage_' + group
        neighborhoods_df[percentage_column] = (
            neighborhoods_df[group_col] / neighborhoods_df['adult_population_total'] * 100
        ).round(2)

    return neighborhoods_df
