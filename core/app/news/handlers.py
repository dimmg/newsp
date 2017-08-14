import datetime
import uuid

from tornado import gen

from ..common import handlers
from ..common.request import application_json, get_json
from ..common.validation import schema
from ..common.utils import paginated_response, slugify
from ..search.config import ESIndex, ESNewsDocType

from .entities import PostEntity


class PostsHandler(handlers.JSONHandler):
    @application_json
    @schema('/news/create.json')
    @gen.coroutine
    def post(self, *args, **kwargs):
        """
        Creates a new 'Post'.
        """
        body = get_json(self.request)
        body.update({
            'uuid': str(uuid.uuid4()),
            'created_at': datetime.datetime.utcnow(),
            'updated_at': datetime.datetime.utcnow(),
            'slug': slugify(body['subject'])
        })

        result = yield self.application.db.news.insert_one(body, callback=None)
        if result:
            self.application.es.index(
                index=ESIndex.news.value, doc_type=ESNewsDocType.post.value,
                body=PostEntity(**body).to_es_payload(), id=body['uuid']
            )

        self.write_json({'_id': str(result.inserted_id)})

    def get(self, id=None, *args, **kwargs):
        if not id:
            return self._get_all_posts()

        return self._get_specific_post(id)

    @gen.coroutine
    def _get_all_posts(self):
        """
        Retrieves all 'Posts'.
        :return: 
        :rtype: dict
        """
        offset = self.get_query_argument('offset', 0)
        limit = self.get_query_argument('limit', 10)

        result = []

        cursor = self.application.db.news.find({}).skip(int(offset)).limit(int(limit))
        count = yield self.application.db.news.find({}).count()

        while (yield cursor.fetch_next):
            post = cursor.next_object()
            result.append(PostEntity.from_persisted(post).to_dict())

        self.write_json(paginated_response(result, count, offset, limit))
        self.finish()

    @gen.coroutine
    def _get_specific_post(self, id):
        """
        Retrieves a specific 'Post'. 
        :param id: 'uuid' of the 'Post' to be retrieved
        :return: 
        :rtype: dict
        """
        post = yield self.application.db.news.find_one({'uuid': id})

        self.write_json(PostEntity.from_persisted(post).to_dict())
