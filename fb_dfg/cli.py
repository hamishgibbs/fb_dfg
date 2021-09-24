import os
import click
import math
import datetime
from fb_dfg import config
from fb_dfg import main
from fb_dfg import utils


@click.group()
def cli():
    pass


@click.command()
@click.option('--partner_id', '-id', help='Facebook Data for Good Partner ID.')
def set_partner_id(partner_id):
    config.set_partner_id(partner_id)


@click.command()
def get_partner_id():
    partner_id = config.get_partner_id()

    if partner_id == "":
        print("No partner ID. Set your partner ID with set-partner-id.")
    else:
        print(f"Partner ID: {partner_id}")


@click.command()
@click.option('--alias_key', '-key', help='Key for dataset alias.')
@click.option('--alias_value', '-value', help='Value for dataset alias.')
def set_alias(alias_key, alias_value):

    config.set_alias(alias_key, alias_value)


@click.command()
@click.option('--alias_key', '-key', help='Key for dataset alias.')
def delete_alias(alias_key):

    config.delete_alias(alias_key)


@click.command()
@click.option('--alias_key', '-key', help='Key for dataset alias.')
def get_alias(alias_key):

    alias_value = config.get_alias(alias_key)

    print(f"Alias: {alias_key} = {alias_value}")


@click.command()
def get_aliases():

    alias_keys = config.get_aliases()

    print(f"\nDataset Aliases: \n\n - {alias_keys}\n")


@click.command()
@click.option('--dataset_id', '-id', help='ID or Alias of Dataset')
@click.option('--start_date', '-start_date', help='Dataset start date (YYYY-MM-DD)')
@click.option('--end_date', '-end_date', help='Dataset end date (YYYY-MM-DD)')
@click.option('--debug', '-debug', default=False, is_flag=True)
def download(dataset_id: str,
             start_date: str,
             end_date: str,
             debug: bool = False):

    
    if dataset_id is None:
        dataset_id = utils.get_dataset_id_auto()

    if start_date is None:
        start_date = utils.get_start_date_auto(dataset_id)
    else:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    if end_date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    path = os.getcwd()

    zip_fn = path + f"/{dataset_id}_data.zip"

    if start_date > end_date:

        raise Exception("start_date must precede end_date.")

    download_len = (end_date - start_date).days

    download_date_seq = [start_date + datetime.timedelta(days=x) for x in range(download_len)]

    processing_sections = utils.chunks(download_date_seq, 30)

    # TODO: double check that this gets all data in original range
    # and that no files are excluded (through main integration tests)
    for section in processing_sections:

        iteration_start_date = min(section)
        iteration_end_date = max(section)

        main.query_data(dataset_id=dataset_id,
                        start_date=iteration_start_date,
                        end_date=iteration_end_date,
                        zip_fn=zip_fn,
                        debug=debug)

        main.unpack_data(dataset_id, zip_fn, path)

        os.remove(zip_fn)


cli.add_command(set_partner_id)
cli.add_command(get_partner_id)
cli.add_command(set_alias)
cli.add_command(delete_alias)
cli.add_command(get_alias)
cli.add_command(get_aliases)
cli.add_command(download)
