import os
import shutil
from fb_dfg import config


def setup_function():

    config_path = os.path.dirname(os.path.realpath(__file__))
    config_path = config_path.replace("tests", "fb_dfg/data")

    if os.path.exists(config_path):

        shutil.rmtree(config_path)


def test_get_config_path_creates_file():

    path = config.get_config_path()

    assert os.path.exists(path)


def test_set_partner_id():

    config.set_partner_id("123")

    path = config.get_config_path()

    data = config.read_config(path)

    assert data["partner_id"] == "123"


def test_get_partner_id():

    config.set_partner_id("123")

    partner_id = config.get_partner_id()

    assert partner_id == "123"


def test_set_alias():

    config.set_alias("KEY", "VALUE")

    path = config.get_config_path()

    data = config.read_config(path)

    assert data["aliases"]["KEY"] == "VALUE"


def test_delete_alias():

    config.set_alias("KEY", "VALUE")

    path = config.get_config_path()

    data = config.read_config(path)

    assert data["aliases"]["KEY"] == "VALUE"

    config.delete_alias("KEY")

    data = config.read_config(path)

    assert list(data["aliases"].keys()) == []


def test_get_alias():

    config.set_alias("KEY", "VALUE")

    assert config.get_alias("KEY") == "VALUE"


def test_get_aliases():

    config.set_alias("KEY", "VALUE")

    assert config.get_aliases() == ["KEY"]
