import requests
import browser_cookie3
from lxml import html
import re
from datetime import datetime
from fb_dfg.cookies import get_cookies

from fb_dfg.config import (get_partner_id,
                           get_alias)

from fb_dfg.unpack import (unzip_file_to_path,
                           get_fn_lookup,
                           rename_files)


def capture_csrf_token(partner_id,
                       headers,
                       data_url: str = "https://partners.facebook.com/data_for_good/data/"):

    token_url = data_url + f"?partner_id={partner_id}"

    page = requests.get(token_url,
                        headers=headers)

    tree = html.fromstring(page.content)

    token_data = tree.xpath('/html/head/script[5]')

    token_re = r'[A-Za-z0-9]{15}:[0-9]{2}:[0-9]{10}'

    # DEV: This is vulnerable to reorganisation of the FB partners page
    token = re.findall(token_re, token_data[0].text)[0]

    return token


def query_data(dataset_id: str,
               start_date: datetime,
               end_date: datetime,
               zip_fn: str,
               partner_id: str = None,
               bulk_url: str = "https://partners.facebook.com/data_for_good/bulk_download/",
               debug: bool = False):

    if not partner_id:
        partner_id = get_partner_id()

    # DEV: need to capture a new CSRF token from the page source before downloading.
    # You can just any CSRF token created by FB on page load (but only temporarily).
    cookie = get_cookies(browser_cookie3.chrome())

    headers = {
        "cookie": cookie
    }

    fb_dtsg = capture_csrf_token(partner_id, headers)

    try:
        dataset_id = get_alias(dataset_id)
    except Exception:
        pass

    query = {"resource_type": "downloadable_csv",
             "partner_id": partner_id,
             "start_date": start_date.strftime("%Y-%m-%d"),
             "end_date": end_date.strftime("%Y-%m-%d"),
             "dataset_id": dataset_id,
             "fb_dtsg": fb_dtsg}

    if debug:
        print("URL: ", bulk_url)
        print("Query: ", query)
        print("Header: ", headers)
        print("CSRF token: ", fb_dtsg)

    res = requests.post(bulk_url,
                        data=query,
                        headers=headers,
                        stream=True)

    # Sometimes the api redirects to a html error page with status 200
    if b"<!DOCTYPE html>" not in res.content:

        with open(zip_fn, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)

        print("Data written to " + zip_fn)

    else:

        raise Exception("Failed to download data.")


def unpack_data(dataset_id: str,
                zip_fn: str,
                path: str):

    unzip_file_to_path(zip_fn, path)

    fn_lookup = get_fn_lookup(path, dataset_id)

    rename_files(fn_lookup)
