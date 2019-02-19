# Greenhouse Tools

Some utility code and scripts for extracting data from Greenhouse's 
[Harvest API](https://developers.greenhouse.io/harvest.html)

Currently this tool can do only one thing - generate an excel file with the anonymized
score card data for a particular job posting.

More information about this can be found [in this spec](https://docs.google.com/document/u/1/d/1iC7na4epL-iu6VPkPMpAXGC9Xy11ZIgZBaGK9KauQOc/edit).

## Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [Python 3](https://www.python.org/downloads/)

It's also recommended that you use a `virtualenv` which will need:

- [Virtualenv](https://virtualenv.pypa.io/en/stable/)
- [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)


## Installation

### Clone repository

```
git clone https://github.com/dimagi/greenhouse-tools.git
```

### Setup Virtualenv (optional but recommended)

```
mkvirtualenv --no-site-packages greenhouse-tools -p python3
```

### Install requirements:

Make sure you are in the root directory of the repository then run:

```
pip install -r requirements.txt
```

## Usage

To use the tool you will first have to find/generate an API key using
[these instructions](https://support.greenhouse.io/hc/en-us/articles/360003470371-Generate-an-API-Key).

Your API key [can be found here](https://app.greenhouse.io/configure/dev_center/credentials)

Then, to run the tool just 

```
python cli.py <api_key> [output file]
``` 

and follow the instructions! If you do not specify an output file, 
your output will be saved to `output/scorecards.csv`.
