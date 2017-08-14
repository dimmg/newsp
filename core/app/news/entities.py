class PostEntity():
    def __init__(self, **kwargs):
        allowed_keys = [
            '_id', 'content', 'created_at', 'image',
            'slug', 'subject', 'updated_at', 'uuid'
        ]

        for key in allowed_keys:
            self.__dict__[key] = kwargs[key]

    @classmethod
    def from_persisted(cls, persisted):
        return cls(
            _id=str(persisted['_id']),
            content=persisted['content'],
            created_at=str(persisted['created_at']),
            image=persisted['image'],
            slug=persisted['slug'],
            subject=persisted['subject'],
            updated_at=str(persisted['updated_at']),
            uuid=str(persisted['uuid'])
        )

    def to_dict(self):
        return self.__dict__

    def to_es_payload(self):
        dict_ = self.__dict__
        dict_.pop('_id')

        return dict_
