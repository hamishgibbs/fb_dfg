import os
import datetime


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_dataset_id_auto():

    cwd = os.getcwd()

    return cwd.split("/")[-1]


def get_start_date_auto(dataset_id, fns=os.listdir(os.getcwd())):

    fn_date_str = [x.replace(dataset_id + "_", "") for x in fns]
    fn_date_str = [x.replace(".csv", "") for x in fn_date_str]

    fn_dates = [datetime.datetime.strptime(x, "%Y_%m_%d_%H%M") for x in fn_date_str]

    start_date = max(fn_dates)

    start_date = start_date + datetime.timedelta(days=1)

    return start_date
