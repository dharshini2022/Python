from orm.metaclass import Meta
from orm.query import Query


class Model(metaclass=Meta):

    def __init__(self, **kwargs):
        for key in self._fields:
            setattr(self, key, kwargs.get(key))

    @classmethod
    def create_table(cls):
        Query.create_table(cls)

    def save(self):
        Query.insert(self)

    @classmethod
    def query(cls):
        return Query(cls)

    @classmethod
    def filter(cls, **kwargs):
        return Query(cls).filter(**kwargs)

    @classmethod
    def all(cls):
        return Query(cls).all()

    @classmethod
    def delete(cls, **kwargs):
        return Query(cls).filter(**kwargs).delete()