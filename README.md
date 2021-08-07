# Yeet DB

A Throwaway Database 🚧

```sql
> make run

> .db # current database

# Use the default db or create your own
> CREATE DATABASE test # create a database

# create a table
> CREATE TABLE person(id int.5 index,name str.100,age int.2)

> .t # List all tables

# Good insert
INSERT INTO person(id,age,name) VALUES(1,23,Abel)
INSERT INTO person(id,age,name) VALUES(2,29,Frank)
INSERT INTO person(id,age,name) VALUES(3,32,Phoebe)

# Bad insert
INSERT INTO person(id,age,name) VALUES(4)
INSERT INTO person(id,age,name) VALUES(5,200,Peppa) # Pigs cant live to 200

# Queries
SELECT * FROM person
# Limit
SELECT id FROM person limit 1
# Filter
SELECT name from person where age > 30
# Operators
SELECT * from person where age < 30 and name = 'Frank'
SELECT * from person where age < 30 or name = 'Frank'
```

A Basic In-Memory database with a very stupid SQL parser