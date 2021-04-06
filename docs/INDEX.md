# Indexing in Yeet

An Index is an additional structure that is derived from the primary data which is used to efficiently find the value for a particular key in the database.

# How to create them ?

```sql
CREATE TABLE <tablename> (
    column1 integer primary_key
    column2 string tree_index
    column3 integer hash_index
)
```

```sql
CREATE KV <tablename> 
```
