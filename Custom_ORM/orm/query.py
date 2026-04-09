from orm.db import db
from orm.fieldDescriptors import ForeignKey

def execute(query, values=None, commit=False, action=None, table=None):
    print()

    if action and table:
        print(f"[{action.upper()}] table={table}")

    print("SQL:", query)

    if values:
        print("VALUES:", values)

    cursor = db.execute(query, values or [])

    if commit:
        db.commit()

    return cursor


class Query:
    def __init__(self, model):
        self.model = model
        self.conditions = []
        self.values = []
        self._order_by = None

    @classmethod
    def create_table(cls, model):
        columns = []
        for name, field in model._fields.items():
            columns.append(f"{name} {field.sql()}")

        query = f"""
        CREATE TABLE IF NOT EXISTS {model._table} (
            {', '.join(columns)}
        )
        """
        execute(query, commit=True, action="create", table=model._table)

   

    @classmethod
    def insert(cls, obj):
        fields = obj._fields.keys()
        values = []
        for f in fields:
            field = obj._fields[f]
            value = getattr(obj, f)
            if isinstance(field, ForeignKey):
                if value is not None:
                    # If user passed object → extract id
                    if hasattr(value, "id"):
                        value = value.id
            values.append(value)
        placeholders = ", ".join(["?"] * len(values))
        field_names = ", ".join(fields)
        query = f"INSERT INTO {obj._table} ({field_names}) VALUES ({placeholders})"
        execute(query, values, commit=True, action="insert", table=obj._table)


    def filter(self, **kwargs):
        for key, value in kwargs.items():
            self.conditions.append(f"{key} = ?")
            self.values.append(value)
        return self


    def order_by(self, field):
        self._order_by = field
        return self

    def _build_query_parts(self):
        query = f"SELECT * FROM {self.model._table}"

        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)

        if self._order_by:
            query += f" ORDER BY {self._order_by}"

        return query, self.values


    def all(self):
        query, values = self._build_query_parts()

        rows = execute(query, values, action="select", table=self.model._table).fetchall()

        return [
            self.model(**dict(zip(self.model._fields.keys(), row)))
            for row in rows
        ]



    def delete(self):
        query = f"DELETE FROM {self.model._table}"

        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)

        execute(query, self.values, commit=True, action="delete", table=self.model._table)


    def update(self, **kwargs):
        set_clause = ", ".join([f"{k} = ?" for k in kwargs])
        values = list(kwargs.values())

        query = f"UPDATE {self.model._table} SET {set_clause}"

        if self.conditions:
            query += " WHERE " + " AND ".join(self.conditions)
            values.extend(self.values)

        execute(query, values, commit=True, action="update", table=self.model._table)


    def __repr__(self):
        return (
            f"<Query model={self.model.__name__}, "
            f"conditions={self.conditions}, "
            f"values={self.values}, "
            f"order_by={self._order_by}>"
        )