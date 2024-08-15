import os
from perigon_news_wrapper import PerigonAPI

def test_query():
    API_KEY = os.environ.get('PERIGON_API_KEY')
    PAGE_SIZE = 100
    api = PerigonAPI(api_key=API_KEY)

    # kwargs:
    payload = {
        'content': 'olympics AND usa AND gold',
        'from': '2024-08-01',
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

    results = api.get_articles(
        paginate=False,
        size=PAGE_SIZE,
        **payload
    )

    assert isinstance(results, list)
    assert len(results) == PAGE_SIZE
    assert isinstance(results[0], dict)