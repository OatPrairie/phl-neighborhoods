from unittest.mock import patch

from census_api.census_data import get_census_block_data
from census_api.constants import COLUMN_MAPPING

MODULE = 'census_api.census_data.'


@patch('census_api.census_data.requests.get')
class TestGetCensusBlockData():
    """ Test get_census_block_data() """

    def test_get_block_data_request_url(self, mock_requests_get):
        """ Test that the correct url is used for the Census API request """
        cols = ",".join(COLUMN_MAPPING.keys())
        expected_url = (
            f'https://api.census.gov/data/2020/dec/dhc?get={cols}'
            f'&for=block:*&in=state:42&in=county:101'
            f'&in=tract:*'
        )

        get_census_block_data()

        mock_requests_get.assert_called_once_with(expected_url)

    def test_get_block_data_remove_empty_blocks(self, mock_requests_get):
        """ Test that blocks with no population are removed """
        mock_requests_get.return_value.json.return_value = [
            ['P1_001N', 'col2', 'col3'],
            ['0', 'col2', 'col3'],
            ['5', 'col2', 'col3'],
            ['21', 'col2', 'col3'],
            ['0', 'col2', 'col3'],
        ]

        expected_data = [
            ['P1_001N', 'col2', 'col3'],
            ['5', 'col2', 'col3'],
            ['21', 'col2', 'col3'],
        ]

        assert get_census_block_data() == expected_data
