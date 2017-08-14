from ..common.handlers import JSONHandler
from ..common.utils import paginated_response
from ..common.validation import schema

from .config import ESIndex, ESNewsDocType
from .service import perform_search


class NewsSearchHandler(JSONHandler):
    def _news_query(self, query_str):
        return {
            'query': {
                'query_string': {
                    'fields': ['subject', 'content'],
                    'query': '**{}**'.format(query_str)
                }
            }
        }

    @schema('/search/news.json')
    def get(self, *args, **kwargs):
        query = self.get_query_argument('query')
        limit = self.get_query_argument('limit', None)
        offset = self.get_query_argument('offset', 0)

        hits, total = perform_search(
            client=self.application.es, query=self._news_query(query),
            indexes=ESIndex.news.value, types=ESNewsDocType.post.value,
            offset=offset, limit=limit
        )

        result = [hit['_source'] for hit in hits]

        self.write_json(paginated_response(result, total, offset, limit))
