# Yeet DB

A Throwaway Database under construction 🚧

```sql
> make run
# person is a pre-created table
# ID - Int(5), NAME - str(100), AGE - int(2)

.t # List all tables

# Good insert
INSERT INTO person(id,age,name) VALUES(1,23,'Abel')
INSERT INTO person(id,age,name) VALUES(2,29,'Frank')
INSERT INTO person(id,age,name) VALUES(3,32,'Phoebe')

# Bad insert
INSERT INTO person(id,age,name) VALUES(4)
INSERT INTO person(id,age,name) VALUES(5,200,'Peppa') # Pigs cant live to 200
INSERT INTO person(id,age,name) VALUES(6,10,Peppa) # Pigs arent objects

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

#### TODO

- Persistence
- Transactions
- Indexing
