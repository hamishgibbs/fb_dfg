import pytest
from datetime import datetime
from fb_dfg import utils


@pytest.fixture()
def expected_clean_fns():

    return ['test_2021_09_01_0800.csv',
            'test_2021_09_01_1600.csv',
            'test_2021_09_01_0000.csv']


def test_get_dataset_id_auto():

    dataset_id = utils.get_dataset_id_auto()

    assert dataset_id == "fb_dfg"


def test_get_start_date_auto(expected_clean_fns):

    start_date = utils.get_start_date_auto("test", fns=expected_clean_fns)

    assert start_date == datetime(2021, 9, 2, 16)
