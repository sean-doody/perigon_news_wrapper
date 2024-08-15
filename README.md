# Perigon API Wrapper
[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

A minimalist Python wrapper for the [Perigon News API](https://www.goperigon.com/). Currently only supports querying all news articles via the `v1/all` endpoint.

Installation (currently, only tested for Python 3.11):

```bash
pip install perigon-news-wrapper
```

## Basic Usage

To initialize the API, import the package and add your API key:

```python
from perigon_news_wrapper import PerigonAPI

# specify your credentials:
api_key = '...'

# initialize API:
api = PerigonAPI(api_key=api_key)

```

The main method is `get_articles()`, which takes the following arguments:

- `paginate [bool = True]`: Whether or not to paginate results (if multiple pages are available). Defaults to `True`.
- `size [int = 100]`: The number of results to return per page. Defaults to `100` (maximum allowed by Perigon).
- `**kwargs`: Arbitrary keyword arguments supported by the Perigon API. Consult the [API docs](https://docs.goperigon.com/reference/all-news) for a comprehensive list of parameters.

`get_articles()` returns a list of dictionaries, where each dictionary is the JSON of an individual article.

**Example:**

```python
# speciy **kwargs (recommend dict format):
payload = {
    'content': 'olympics AND usa AND gold',
    'from': '2024-07-26',
    'to': '2024-08-08',
    'language': 'en', 
    'exclude_labels': [
        'Non-news',
        'Opinion',
        'Fact Check',
        'Roundup',
        'Low Content'
    ]
}

# get results, using payload as **kwargs:
results = api.get_articles(paginate=False, size=100, **payload)
```

## TODO
- [ ] Establish tests for other Python versions (only tested on Python 3.11).
- [ ] Add support for querying additional Perigon endpoints.
- [ ] Add support for parsing/saving results?