import os
import errno
import json


def write_config(config_path, config={"partner_id": "", "aliases": {}}):

    with open(config_path, "w") as f:

        json.dump(config, f)


def read_config(config_path):

    with open(config_path, "rb") as f:

        config = json.load(f)

    return config


def get_config_path():
    # Get config file location (or create if it doesn't exist)

    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "data", "config.json")

    if not os.path.exists(os.path.dirname(config_path)):
        try:
            os.makedirs(os.path.dirname(config_path))

            write_config(config_path)

            print(f"Created empty configuration at {config_path}.")

        except OSError as exc:
            if exc.errno != errno.EEXIST:
                msg = f"Unable to create a configuration file at {config_path}"
                raise Exception(msg)

    return config_path


def set_partner_id(partner_id):
    # set partner id for the whole package in a config file

    config_path = get_config_path()
    config = read_config(config_path)

    config["partner_id"] = partner_id

    write_config(config_path, config)

    print(f"Partner ID saved: {partner_id}")


def get_partner_id():

    config_path = get_config_path()

    config = read_config(config_path)

    return config["partner_id"]


def set_alias(alias_key, alias_value):
    # set a dataset alias for the whole package in a config file

    config_path = get_config_path()

    config = read_config(config_path)

    config["aliases"][alias_key] = alias_value

    write_config(config_path, config)

    print(f"Dataset alias saved. {alias_key} = {alias_value}")


def delete_alias(alias_key):

    config_path = get_config_path()

    config = read_config(config_path)

    config["aliases"].pop(alias_key, None)

    write_config(config_path, config)

    print(f"Dataset alias deleted. {alias_key}")


def get_alias(alias_key):

    config_path = get_config_path()

    config = read_config(config_path)

    return config["aliases"][alias_key]


def get_aliases():

    config_path = get_config_path()

    config = read_config(config_path)

    return list(config["aliases"].keys())
