from orm.db import db
from orm.metaclass import Meta

class Model(metaclass=Meta):

    def __init__(self, **kwargs):
        for key in self._fields:
            setattr(self, key, kwargs.get(key))

    @classmethod
    def create_table(cls):
        columns = []
        for name, field in cls._fields.items():
            columns.append(f"{name} {field.sql()}")

        query = f"CREATE TABLE IF NOT EXISTS {cls._table} ({', '.join(columns)})"
        db.execute(query)

    def save(self):
        fields = self._fields.keys()
        values = [getattr(self, f) for f in fields]

        placeholders = ", ".join(["?"] * len(values))
        field_names = ", ".join(fields)

        query = f"INSERT INTO {self._table} ({field_names}) VALUES ({placeholders})"
        db.execute(query, values)

    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls._table}"
        rows = db.execute(query).fetchall()

        results = []
        for row in rows:
            obj = cls(**dict(zip(cls._fields.keys(), row)))
            results.append(obj)

        return results

    @classmethod
    def filter(cls, **kwargs):
        conditions = []
        values = []

        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            values.append(value)

        where_clause = " AND ".join(conditions)

        query = f"SELECT * FROM {cls._table} WHERE {where_clause}"
        rows = db.execute(query, values).fetchall()

        return [cls(**dict(zip(cls._fields.keys(), row))) for row in rows]