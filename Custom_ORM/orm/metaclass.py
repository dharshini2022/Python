from orm.fieldDescriptors import Field, ForeignKey

class Meta(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        foreign_keys = {}

        for key, value in attrs.items():
            if isinstance(value, ForeignKey):
                foreign_keys[key] = value
                fields[key] = value
            elif isinstance(value, Field):
                fields[key] = value

        attrs["_fields"] = fields
        attrs["_foreign_keys"] = foreign_keys
        attrs["_table"] = name.lower()

        new_class = super().__new__(cls, name, bases, attrs)

        for key, fk in foreign_keys.items():
            related_name = f"{name.lower()}_set"

            if not hasattr(fk.to, "_reverse_relations"):
                fk.to._reverse_relations = {}

            fk.to._reverse_relations[related_name] = (new_class, key)

        return new_class