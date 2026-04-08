class Field:
    def __init__(self, nullable=False, unique=False):
        self.name = None
        self.nullable = nullable
        self.unique = unique

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
        return f"VARCHAR({self.max_length})"


class IntegerField(Field):
    def sql(self):
        return "INTEGER"