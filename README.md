# fb_dfg: automate downloads from Facebook Data for Good

[![GitHub Actions (tests)](https://github.com/hamishgibbs/fb_dfg/actions/workflows/tests.yml/badge.svg)](https://github.com/hamishgibbs/fb_dfg)

`fb_dfg` automates downloading from the Facebook Data For Good Partner Program Platform. Because Facebook does not provide an API to download data from the Partner Platform, use `fb_dfg` to simulate the behaviour of an API for downloading datasets and automatically updating data collections. For a previous version of this library (now deprecated) see [pull_facebook_data_for_good](https://github.com/hamishgibbs/pull_facebook_data_for_good).

*Disclaimer: This library will only work for users with access to the Facebook Data for Good Partner Program, and will only function for datasets to which the user has been granted access. This tool is not developed by or associated with Facebook.*

## Features:

* Uses cached authentication credentials.
* Allows access to data with custom aliases.
* Exposes CLI commands to incrementally update data collections.

## Installation

**From a clone:**

To develop this project locally, clone it onto your machine:

```{shell}
git clone https://github.com/hamishgibbs/fb_dfg.git
```

Enter the project directory:

```{shell}
cd fb_dfg
```

Install the package with:

```{shell}
pip install .
```

**From GitHub:**

To install the package directly from GitHub run:

```{shell}
pip install git+https://github.com/hamishgibbs/fb_dfg.git
```

## License

[MIT License](https://github.com/hamishgibbs/fb_dfg/blob/main/LICENSE)

## Quick Start

The easiest way to use `fb_dfg` is from the command line. See documentation for command line functions with:

```{shell}
fb_dfg --help
```

**Setup:**

Downloading data from the Facebook Data For Good platform requires two components:

* Partner ID (Your own partner ID)
* Dataset ID (The ID of the dataset you want to download)

`fb_dfg` will save these values in a configuration file locally. Set your partner ID with:

```{shell}
fb_dfg set-partner-id -id 1234567890
```

Data for Good Datasets are referenced with a numeric ID. You can create a human-readable alias for a Dataset ID with:

```{shell}
fb_dfg set-alias -key Britain_TileMovement -value 1234567890
```

To find your partner ID, look in the base url of the Portal home page.

To find a Dataset ID, look in the url of the portal when you have selected a dataset. Use the `activeDatasetID`.

**Downloading Data:**

You can use the CLI to download a dataset in a certain date range with the `download` function:

```{shell}
fb_dfg download -id Britain_TileMovement -start_date "2021-01-01" -end_date "2021-02-01" --debug
```

Using the `--debug` flag provides more details about your data request and authentication credentials.

Downloading uses authenticated cookies stored locally. You must be authenticated with the Portal before downloading data. You will be prompted for your password to give `fb_dfg` access to your authentication cookies. If you would like to use `fb_dfg` without authenticating for each download, use the internal download function in `main/query_data.py` with a properly formatted cookie string.

**Updating a Data Collection:**

In the special case of updating an existing data collection with the latest data, `cd` into the directory where the data is stored and use:

```{shell}
fb_dfg download
```

`fb_dfg` will automatically construct a query with the appropriate parameters. Note that the parent folder of the data collection MUST be a recognized dataset alias.

## Limitations

`fb_dfg` only supports cookies from Chrome. You must authenticate with the Portal with Chrome to use the library.

`fb_dfg` was tested with Python 3.7 on Mac and Linux.

Data queries of >30 days do not return data from the Portal. To address this, `fb_dfg` breaks queries >30 days into 30 day "chunks". In practice, the Portal begins to reject the 3rd - 4th successive data query. It is recommended that you limit the length of dataset queries by updating dataset collections regularly.

## Contributions

Contributions are welcome! If you see a problem with the library, please [open an issue](https://github.com/hamishgibbs/fb_dfg/issues/new).
