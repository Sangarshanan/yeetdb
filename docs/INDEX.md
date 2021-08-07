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
select * from table where age > 10
```

- Figure out the columns with indexes i.e Age
- Goto the Tree Index file of Age and figure all the keys whose value is greater than 10, the
value will give you the pk of the table so records with age > 10 are from ID (1,2,3,4)
- Now we head to our actual table where we use the pk location to performed an Indexed Scan to fetch all record values for 
the given set of keys and then return it
- If the column being filtered is not indexed then we have to scan thro every record of the table and apply the filter, these full scans are expensive
