import pytest
import os
import shutil
from fb_dfg import unpack


@pytest.fixture()
def tmp_path():

    return os.path.dirname(os.path.realpath(__file__)) + "/tmp_data"


@pytest.fixture()
def expected_raw_fns():

    return [
        '111111111111111_2021-09-01_0000.csv',
        '111111111111111_2021-09-01_0800.csv',
        '111111111111111_2021-09-01_1600.csv']


@pytest.fixture()
def expected_clean_fns():

    return [
        'test_2021_09_01_0800.csv',
        'test_2021_09_01_1600.csv',
        'test_2021_09_01_0000.csv']


def setup_function():

    test_path = os.path.dirname(os.path.realpath(__file__))

    tmp_data_path = test_path + "/tmp_data"

    test_data_path = test_path + "/data/test_data.zip"

    os.mkdir(tmp_data_path)
    shutil.copy(test_data_path, tmp_data_path)


def teardown_function():

    test_path = os.path.dirname(os.path.realpath(__file__))

    tmp_data_path = test_path + "/tmp_data"

    shutil.rmtree(tmp_data_path)


def test_unzip_file_to_path(tmp_path, expected_raw_fns):

    unpack.unzip_file_to_path(tmp_path + "/test_data.zip",
                              tmp_path)

    print(os.listdir(tmp_path + "/test_data"))

    assert os.listdir(tmp_path + "/test_data") == expected_raw_fns


def test_rename_unzipped_files(tmp_path, expected_clean_fns):

    unpack.unzip_file_to_path(tmp_path + "/test_data.zip",
                              tmp_path)

    fn_lookup = unpack.get_fn_lookup(tmp_path + "/test_data", "test")

    # check that tuple hour pairs match
    assert fn_lookup[0][0][-8:] == fn_lookup[0][1][-8:]
    assert fn_lookup[1][0][-8:] == fn_lookup[1][1][-8:]
    assert fn_lookup[2][0][-8:] == fn_lookup[2][1][-8:]

    unpack.rename_files(fn_lookup)

    print(os.listdir(tmp_path + "/test_data"))

    obs_clean_fns = os.listdir(tmp_path + "/test_data")

    assert sum([x in obs_clean_fns for x in obs_clean_fns]) == 3
