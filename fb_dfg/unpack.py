import os
import zipfile
import re
import glob


def unzip_file_to_path(zip_fn, path):

    with zipfile.ZipFile(zip_fn, 'r') as zip_ref:
        zip_ref.extractall(path)


def get_fn_lookup(path, dataset_id):

    files = glob.glob(path + "/*.csv")

    fn_re = r"/[0-9]{15}_"

    id_rep = [re.sub(fn_re, "/" + dataset_id + "_", x) for x in files]

    date_rep = [x[:-19] + re.sub("-", "_", x[-19:]) for x in id_rep]

    return tuple(zip(files, date_rep))


def rename_files(fn_lookup):

    for old_fn, new_fn in fn_lookup:

        if old_fn != new_fn:

            os.rename(old_fn, new_fn)
