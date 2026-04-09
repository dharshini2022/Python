**PYTHON ORM WITH SQLite**

**Overview**
This project is a lightweight Object-Relational Mapper (ORM) built from scratch using Python. It mimics core ORM functionality such as model definition, query building, relationships, and lazy loading — without using external libraries like Django ORM or SQLAlchemy.

The goal is to deeply understand how ORMs work internally by implementing:

* Metaclasses for model parsing
* Descriptors for field handling
* SQL generation
* Query abstraction
* Relationships with lazy loading

**Features**
*Define database tables as Python classes
* Automatic SQL table creation
* CRUD operations (insert, select, update, delete)
* Query chaining (filter().order_by().all())
* Foreign key relationships
* Reverse relations (user.post_set)
* Lazy loading of related objects
* SQL query logging in console

**Project Strucutre**
orm/
│── db.py                  # Database connection handler
│── fieldDescriptors.py    # Field & descriptor logic
│── metaclass.py           # Model parsing & relationship setup
│── model.py               # Base Model class
│── query.py               # Query builder & executor
│── database.db            # SQLite database
main.py                    # Example usage

**Core Components**
1) Model (model.py)
It is the Base class for all models. It provides:
* .create_table()
* .save()
* .filter()
* .all()
* .delete()
It also handles reverse relationships dynamically using __getattr__.

2) Metaclass (metaclass.py)
Responsible for:
* Extracting fields from model classes
* Identifying foreign keys
* Creating: _fields, _foreign_keys, _table
* Setting up reverse relations
Example: 
User -> Post, automatically creates: user.post_set

3) Field Descriptors (fieldDescriptors.py)
Defines the interaction with data or fields (columns of the table).
**Field Types:**
* IntegerField
* CharField
* ForeignKey

Responsibilities:
* Validation (nullable, unique, primary_key)
* SQL generation
* Attribute access control

4) Query Builder (query.py)
Handles:
* SQL generation
* Query chaining
* Execution

Supports:
User.filter(age=21).order_by("name").all()

Operations:
* SELECT
* INSERT
* UPDATE
* DELETE

5) Database Layer (db.py)
Simple wrapper over sqlite3:
* Manages connection
* Executes queries
* Commits transactions

**WORKFLOW**
**STEP 1: Model Definition**
class User(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    age = IntegerField()

class Post(Model):
    id = IntegerField(primary_key=True)
    title = CharField(max_length=100)
    user_id = ForeignKey(User)

Metaclass processes this and:
* Registers fields
* Creates table name (user, post)
* Links relationships

**STEP 2: TABLE CREATION**
User.create_table()
Post.create_table()

Generated SQL:
CREATE TABLE IF NOT EXISTS user (...);
CREATE TABLE IF NOT EXISTS post (...);

**STEP 3: Insert Data**
u1 = User(id=1, name="Dharshini", age=21)
u1.save()

SQL:
INSERT INTO user (id, name, age) VALUES (?, ?, ?)

**STEP 4: Query Data**
users = User.filter(age=21).all()

SQL:
SELECT * FROM user WHERE age = 21

STEP 5: Update Data
User.filter(name="Dharshini").update(age=100)

SQL:
UPDATE user SET age = 100 WHERE name = 'Dharshini'

**STEP 6: Delete Data**
User.delete(name="Alex")

SQL:
DELETE FROM user WHERE name = 'Alex'

**STEP 7: Relationships (Lazy Loading)**
user.post_set

SQL:
SELECT * FROM post WHERE user_id = <user.id>

**RELATIONSHIPS**
FORWARD RELATION (Post -> User)
* (child -> Parent)
* It uses the foreign key to get the user details
* A Post has a pointer (user_id) → forward
post.user_id
Meaning: “This post belongs to which user?”

REVERSE RELATION (User -> Post)
(Parent -> Child)
* It works by finding all rows that references the parent (search with respect to primary key)
* A User doesn’t store posts, but you search for them → reverse
user.post_set
Meaning: “Which posts belong to this user?”

These relations are useful to fetch details with respect to object navigation instead of sql

**LAZY LOADING**
* Data is fetched only when you actually access it, not before.

Without Lazy Loading:
users = User.all()
If this is triggered, this will fetch all the users and posts details

With Lazy Loading:
user.post_set     ==> users = User.all()
This would fetch only user details, not the details of linked tables (Post) as well.
