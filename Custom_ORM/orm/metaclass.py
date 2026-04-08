from orm.fieldDescriptors import Field

class Meta(type):
    def __new__(cls, name, bases, attrs):
        if(name == "Model"):
            return super().__new__(cls, name, bases, attrs)
    
        fields = {}

        for key,value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value
            
        attrs["_fields"] = fields
        attrs["_table"] = name.lower()

        return super().__new__(cls, name, bases, attrs)
