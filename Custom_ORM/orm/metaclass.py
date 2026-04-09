from orm.fieldDescriptors import Field

class Meta(type):
    def __new__(cls, name, bases, attrs):
        if(name == "Model"):
            return super().__new__(cls, name, bases, attrs)
    
        fields = {}
        foreign_keys = {}

        for key,value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
            # elif isinstance(value, ForeignKey):
            #     foreign_keys[key] = value
            
        attrs["_fields"] = fields
        attrs["_foreign_keys"] = foreign_keys
        attrs["_table"] = name.lower()

        return super().__new__(cls, name, bases, attrs)
