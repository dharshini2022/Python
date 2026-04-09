class Field:
    def __init__(self, nullable=False, unique=False,  primary_key=False):
        self.name = None
        self.nullable = nullable
        self.unique = unique
        self.primary_key = primary_key

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not self.nullable and value is None:
            raise ValueError(f"{self.name} cannot be null")
        instance.__dict__[self.name] = value


class CharField(Field):
    def __init__(self, max_length, **kwargs):
        super().__init__(**kwargs)
        self.max_length = max_length

    def sql(self):
        parts = [f"VARCHAR({self.max_length})"]

        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")

        return " ".join(parts)


class IntegerField(Field):
    def sql(self):
        parts = ["INTEGER"]

        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")

        return " ".join(parts)
    
class ForeignKey(Field):
    def __init__(self, to, **kwargs):
        super().__init__(**kwargs)
        self.to = to 

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__.get(self.name)
        if value is None:
            return None
        return self.to.filter(id=value).all()[0]
    
    def get_id(self, instance):
        return instance.__dict__.get(self.name)

    def sql(self):
        referenced_table = self.to._table

        parts = ["INTEGER"]

        if not self.nullable:
            parts.append("NOT NULL")

        parts.append(f"REFERENCES {referenced_table}(id)")

        return " ".join(parts)