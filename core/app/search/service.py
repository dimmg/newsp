import os
import json

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError

from . import config

MAPPINGS_DIR = os.getcwd() + '/app/search/mappings'
ASCII_FOLDING_TOKEN_FILTER = {
    "analysis": {
        "analyzer": {
            "default": {
                "tokenizer": "standard",
                "filter": ["lowercase", "asciifolding"]
            }
        }
    }
}


def get_index_mappings(index):
    """
    Returns mappings for a specific index.
    :param index: index name
    :return: index mappings
    :rtype: dict
    """
    with open(MAPPINGS_DIR + index + '.json', 'r') as f:
        return json.load(f)


def set_index_settings(mappings, settings=None):
    return {
        'settings': settings or ASCII_FOLDING_TOKEN_FILTER,
        'mappings': mappings
    }


def _setup_indexes_settings(client):
    if not client.indices.exists(index=config.ESIndex.news.value):
        index_settings = set_index_settings(mappings=get_index_mappings(config.ESIndex.news.value))
        client.indices.create(index=config.ESIndex.news.value, body=index_settings)


def init_es_client():
    """
    Initializes an Elasticsearch client.
    
    It is recommended to use this function only once,
    thus reusing the same client for every request.
    :return: Elasticsearch client
    """
    client = Elasticsearch(
        ['elasticsearch'], port=9200,
        http_auth=('elastic', 'changeme')
    )

    _setup_indexes_settings(client)

    return client


def perform_search(client, query, indexes=None, types=None, offset=None, limit=10):
    """
    Returns hits and hits count for specific query.
    :return: 
    """
    try:
        res = client.search(
            index=indexes,
            doc_type=types,
            from_=offset,
            size=limit,
            body=query
        )

        return res['hits']['hits'], res['hits']['total']

    except (NotFoundError, RequestError) as e:
        raise Exception(str(e))
