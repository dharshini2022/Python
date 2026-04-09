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
    
    def __getattr__(self, item):
        relations = getattr(type(self), "_reverse_relations", {})

        if item in relations:
            model_class, field = relations[item]

            pk = getattr(self, "id", None)
            if pk is None:
                return []

            return model_class.filter(**{field: pk}).all()

        raise AttributeError(f"{item} not found")