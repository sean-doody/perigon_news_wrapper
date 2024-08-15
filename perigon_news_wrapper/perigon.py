import sys
import math
import logging
from tqdm import tqdm

import requests
from requests.exceptions import RequestException
from tenacity import retry, wait_exponential, stop_after_attempt

# logger:
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class PerigonAPI:
    '''
    A minimalist API wrapper for the Perigon News API. Currently, performs the basic function
    of collecting articles from Perigon's /v1/all API endpoint. Articles will be returned
    as a list of dictionaries when calling the get_articles() method.

    Attributes:
        api_key (str): Your Perigon API key.
        endpoint (str): URL to the /v1/all API endpoint.

    Methods:
        get_articles: Collects articles from the Perigon /v1/all API endpoint. Returns them
                      as a list of dicts.
    '''
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = 'https://api.goperigon.com/v1/all'

    def get_articles(
        self, paginate: bool = True, size: int = 100, **kwargs
    ) -> list[dict]:
        '''
        Collects results from Perigon's /v1/all API endpoint.

        Args:
            paginate (bool): whether or not to paginate results. Defaults to True. If set
                             to false, only the first page of results is returned. Otherwise,
                             it will fetch all remaining pages.
            size (int): the number of results to return per page. Maximum of 100.
            **kwargs: Arbitrary and variable keywords arguments suitable to the selected
                      endpoint. Consult the Pergion documentation for a list of endpoint parameters:
                            https://docs.goperigon.com/docs/getting-started
                      Note: if using multiple values of the same parameter, pass these as a list, e.g.:
                            topics = ['Crime', 'Social Issues']
        '''

        # validate kwargs:
        if 'size' in kwargs.keys():
            kwargs['size'] = None

        if 'page' in kwargs.keys():
            kwargs['page'] = None

        # headers and parameters:
        headers = {'x-api-key': self.api_key}
        payload = {k: v for k, v in kwargs.items() if v is not None}
        payload['size'] = size

        # get results:
        results = []

        logger.info('Executing initial query with kwargs: %s', kwargs)
        initial_response = self._get_request(
            url=self.endpoint, headers=headers, params=payload
        )
        results.extend(initial_response['articles'])

        # paginate:
        if paginate:
            total_articles = initial_response['numResults']
            if total_articles > size:
                pages = math.ceil(total_articles / size)
                remaining_pages = pages - 1

                logger.info('Pages to paginate: %s', remaining_pages)
                with tqdm(total=remaining_pages, desc='Progress', unit='page') as pbar:
                    for page in range(1, pages):
                        payload['page'] = page
                        response = self._get_request(
                            url=self.endpoint, headers=headers, params=payload
                        )
                        results.extend(response['articles'])
                        pbar.update(1)

        return results

    @staticmethod
    @retry(
        stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=2, max=30)
    )
    def _get_request(url: str, headers: dict, params: dict, timeout: int = 60) -> dict:
        try:
            response = requests.get(
                url=url, headers=headers, params=params, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except RequestException as err:
            logger.error('Request failed: %s', err)