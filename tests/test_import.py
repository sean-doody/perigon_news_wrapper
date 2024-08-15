import os
from perigon_news_wrapper import PerigonAPI

def test_import():
    API_KEY = os.environ.get('PERIGON_API_KEY')
    api = PerigonAPI(api_key=API_KEY)
    assert api.api_key is not None