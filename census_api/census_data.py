import requests

from census_api.constants import COLUMN_MAPPING


def get_census_block_data(tract: str = '*', block: str = '*') -> list:
    """
    Get block data from Census API with headers while removing unpopulated blocks
    """
    year = '2020'
    dsource = 'dec' # the survey i.e. decennial census, acs, etc
    dseries = 'dhc' # a dataset within the survey
    state = '42' # PA
    county = '101' # Philadelphia

    # Variables from https://api.census.gov/data/2020/dec/dhc/variables.json
    cols = ",".join(COLUMN_MAPPING.keys())

    base_url = f'https://api.census.gov/data/{year}/{dsource}/{dseries}'
    data_url = (
        f'{base_url}?get={cols}&for=block:{block}&in=state:{state}&in=county:{county}'
        f'&in=tract:{tract}'
    )
    resp = requests.get(data_url)
    data = resp.json()
    # The first element of the list returned from the Census API contains the requested column names
    data_columns = data[0]
    total_population_idx = data_columns.index('P1_001N')
    data[:] = [block for block in data[1:] if int(block[total_population_idx])]
    data.insert(0, data_columns)

    return data
