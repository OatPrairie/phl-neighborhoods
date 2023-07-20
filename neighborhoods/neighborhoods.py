import os
from datetime import datetime
from dateutil import tz

import pandas as pd
from flask import Blueprint, redirect, render_template, Response

from census_api.constants import COLUMN_MAPPING
from data_processing.data_processing import (
    get_neighborhood_demographics,
    download_census_block_data,
)

neighborhoods_bp = Blueprint(
    'neighborhoods_bp',
    __name__,
    template_folder='templates'
)


@neighborhoods_bp.route('/', methods=['GET'])
def neighborhoods_home() -> Response:
    path = 'data_sets/census_block_data.csv'

    if not os.path.exists(path):
        download_census_block_data()

    census_block_df = pd.read_csv(path)
    local_tz = tz.tzlocal()
    last_modified_timestamp = os.path.getmtime(path)
    last_modified_dt = datetime.fromtimestamp(last_modified_timestamp).astimezone(local_tz)
    last_modified_on = last_modified_dt.strftime('%Y-%m-%d %H:%M:%S')
    neighborhoods_df = get_neighborhood_demographics(census_block_df)
    neighborhoods_df = neighborhoods_df.reset_index()
    neighborhoods = neighborhoods_df.to_dict('records')

    return render_template(
        'neighborhoods_home.html',
        last_modified_on=last_modified_on,
        neighborhoods=neighborhoods,
    )

@neighborhoods_bp.route('/refresh_census_block_data', methods=['GET'])
def refresh_census_block_data() -> Response:
    download_census_block_data()

    return redirect('/neighborhoods')
