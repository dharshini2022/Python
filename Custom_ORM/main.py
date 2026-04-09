from orm.model import Model
from orm.fieldDescriptors import IntegerField, CharField, ForeignKey

class User(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    age = IntegerField()


class Post(Model):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=100)
    user_id = ForeignKey(User)


User.create_table()
Post.create_table()

u1 = User(id=1, name="Dharshini", age=21)
u1.save()

u2 = User(id = 2, name = "Alex", age = 35)
u2.save()

p1 = Post(id=1, title="Hello ORM", user_id=1)
p1.save()

print("\n--- FILTER ---")
users = User.filter(age=21).all()
for user in users:
    print(user.name, user.age)


print("\n--- UPDATE ---")
User.filter(name="Dharshini").update(age=100)


updated_users = User.filter(name="Dharshini").all()
for user in updated_users:
    print("Updated:", user.name, user.age)


print("\n--- DELETE ---")
User.delete(name="Alex")
print("After Deletion")
updated_users = User.all()
for user in updated_users:
    print( user.name, user.age)

print("\n--- USER → POSTS RELATIONSHIP ---")

users = User.all()

for user in users:
    print(f"User: {user.name} ({user.age})")

    posts = user.post_set

    if not posts:
        print("  ↳ No posts")
    else:
        for post in posts:
            print(f"  ↳ Post: {post.title}")