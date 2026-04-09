from orm.model import Model
from orm.fieldDescriptors import IntegerField, CharField

class User(Model):
    id = IntegerField()
    name = CharField(max_length = 100)
    age = IntegerField()

# User.create_table()

# u1 = User(id=1, name="Dharshini", age=21)
# u1.save()

# u2 = User(id=2, name="Alex", age=25)
# u2.save()

users = User.all()
for user in users:
    print(user.name, user.age)

filtered = User.filter(age=21).all()

for user in filtered:
    print("Filtered:", user.name)