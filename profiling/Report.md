# SQLite vs MongoDB #

To run my function, uncomment them in each file. They were pre-written for you.

The first optimization is stores the contents of the csv files into two lists, `accounts` and `statuses`.
That'll make it significantly faster to load the data into my databases.

## PyMongo: Method for Optimization ##
For Pymongo, I tested the performance gains with insert_many, delete_many and update_many.
I inserted one user, inserted 200k statuses, deleted one user, deleted their 100+ statuses,
updated one user, and changed the status_text for 100+ statuses. I also compared find_one to
search for one user, and find() to search for multiple statuses.

Worth noting is that the more parameters you pass in a function, the slower it runs. Update_
one_user was surprisingly slower even though we are only updating one user.
I suspect that search_many_statuses_by_user_id (self-explanatory) took the longest because the find 
method scans the entire table. MongoDB tries to prevent needless querying, so it must be made to
to keep querying. As opposed to find_one because it'll only return the first document.
and also supports querying on specific elements, in that case user_id. That is truly the strength of
MongoDB, is its search indexing. It can create an index out of any field. 

I also experimented with the number of statuses, and compared insert_many loading just 2 users and
4 statuses, and loadings 1000x more accounts, for instance. Adding 1000x more accounts takes 100x 
longer than just added 2. Adding 500x more statuses takes 460x time longer than just adding 4. 
Therefore, adding 10x more after the first 2k rows quadruples the time it takes. 

## Peewee: Method for Optimization ##

What I liked about using peewee's chunked method is that I don't have to create a dictionary key. 
For it to work, I did have to go in accounts.csv and status_updates.csv and change the headers 
to match my peewee model fieldnames. Likewise, for my pymongo code; Python dictionaries are case-
sensitive. 

It's faster to search with peewee because we select on a condition met. 

I had to make sure to re-add the user that I had deleted to avoid getting blocked by the foreignkey 
constraint. `status_updates.csv` has 10x more rows than `accounts.csv` (~200k rows). In the future,
I'd like to play with the batch size to see if it improves performance. It took 8578.42 ms to load 
my status data onto my table. That's 85x slower than the 2k rows of user data I uploaded. It also
took double the time than it took pymongo to load up the data, but comparable for the first 2k.

Deleting, searching and updating multiple records was faster for peewee than pymongo. 5-6x faster for
deleting and updating. And 10x faster for searching. This is likely owed by the complex queries I wrote for 
peewee. It's easy to do a select.where.

Since it couldn't find Keri.Royce8, it was faster at  returning a benchmark time. For `Roshelle.Pironi69` 
it took a bit longer because I asked to print each status_id for the 95 messages my query found. 
When I simply counted how many messages, as opposed to counting them, it took only 9.88 ms instead of 
20 ms. So printing is expensive.


### Performance results ###
If you see some blank cells, it is because I wanted to more easily specify the number of records retrieved by the 
function as it is likely to affect the performance of pymongo or peewee. 

| Task                                                                            | SQLite      | MongoDB      |
|---------------------------------------------------------------------------------|-------------|--------------|
| benchmark_load_one (2k users, peewee: create, pymongo: insert_one)              | 14.34 ms    | 51.05 ms     |
| benchmark_load_many (2k users in bulk, peewee: chunked, pymongo: insert_many)   | 116.14 ms   | 103.71 ms    |
| benchmark_load_many (200k statuses in bulk, pw: chunked, pymongo: insert_many)  | 8578.42ms   | 3449.88 ms   |
| benchmark_add_row (peewee: create, pymongo: insert_many, can add multiple)      | 8.14 ms     | 9.93 ms      |
| benchmark_add_row (peewee: create, pymongo: insert_many, can add multiple)      | 8.39 ms     | 7.61 ms      |
| benchmark_search_one_user (pymongo: find_one, peewee: get)                      | 1.29 ms     | 8.78 ms      |
| benchmark_search_many_statuses_by_user_id (pymongo: find, peewee: select.where) | 20.77ms     | 215.38 ms    |
| benchmark_fuzzy_search_many_statuses_by_user_id (pymongo: 47,558 statuses)      |             | 378 ms       |
| benchmark_fuzzy_search_status(peewee: 393 statuses)                             | 39.77 ms    |              |
| benchmark_update_one_user (pass 5 parameters)                                   | 4.28 ms     | 89.75 ms     |
| benchmark_update_many_statuses (3 statuses,  update_many, pymongo)              |             | 9.4 ms       |
| benchmark_update_many_statuses (182 statuses, pymongo)                          |             | 354.85 ms    |
| benchmark_update_many_statuses (121 statuses, peewee)                           | 59.37 ms    |              |
| benchmark_delete_one_user (peewee: delete_instance, pymongo: delete_one)        | 4.76 ms     | 12.71 ms     |
| benchmark_fuzzy_delete_many_users (203 users starting with user_name: 'A')      |             | 12.03 ms     | 
| benchmark_delete_many_statuses (3 statuses, pymongo: delete_many)               |             | 15.56 ms     |
| benchmark_delete_many_statuses (242 statuses, pymongo: delete_many )            |             | 559.09 ms    |
| benchmark_delete_many_statuses (100 statuses, peewee: delete.where)             | 49.9 ms     |              |



# Side by side comparisons of each function #

### Loading by the row ###
Pymongo: Insert_one from csv data stored in a list in memory took Pymongo 51.05 ms! 
That's 5x more than if I use insert_many.

Peewee: Loading one row in peewee required instantiating a collection and using the add_user function
using a for loop and specifying the order of the variables to match the indexes in add_user. It is
significantly faster than pymongo's insert_one method, 14.34 ms and only slightly slower than insert_many.
add_user called peewee's create method on UsersTable. 

### Loading in bulk ###
Pymongo: I used insert_many to add multiple users and statuses. The performance is comparable to the
chunked method I used for peewee, at 103 ms. 

Peewee: I used the chunked method to add the status data in batches. The performance was about the same,
roughly 116 ms.

### Adding one row ###
Pymongo: I keep the same add_row function to add both a user and a status. Unlike peewee, I don't have to 
create a key, as long as I can pass the values as parameters and specify a table. It took less than 10 ms
for a couple of rows.

Peewee: I have to create a key, and pass the parameters in the correct order then save() to add a row. 
For that reason, I had to create two different functions. I use the create method to add a row, and unlike
pymongo I cannot use insert_many to add multiple records. The performance of both peewee and pymongo are
comparable, but peewee can only add one row at a time and needs a key. It's very strict. 

### Updating one ###
Pymongo: I chose to update_one row in the `insert_many_users` table. It was relatively slower, at 89.75 ms. 

Peewee: I used the get method in my update_one_user function. It was 22x faster than pymongo's update_one. 

### Updating many ###
Pymongo: This was an elegant function. I used update_many and the $set operator to replace the value of the
status_text field for a specific user_id. In this case, I overwrote status_texts by Jaclyn.Lola99 with the 
message "Who-ville". For 182 statuses, it took 354 ms. For the original 3 Dr.Seuss messages I added separate
from the dataset, the task took 9.4 ms. 

Peewee: I wrote a query and used update().where to filter the statuses by user_id and overwrite all the
status_texts with "I am Nadiya". It's 7x faster, and took 59 ms to update 121 statuses. 

### Deleting one ###
Pymongo: I used delete_one, which took 3x longer than peewee. 12 ms. 

Peewee: I used the get method and delete_instance() method. It took 4 ms. 

### Deleting many ###
Pymongo: I used delete_many, it took 5x longer than peewee. Anywhere from 331 to 559 ms for ~200 statuses.
I tried delete_one on multiple records, but pymongo wouldn't allow it. But I did try to delete 203 users
using a fuzzy search delete_many({'user_name': {'$regex': user_name}) and it is significantly faster when it
doesn't have to jump from place to place in the table looking for that one user. The search criteria was:
any user_name that starts with the letter A. It took 12 ms, about the same amount of time as deleting 3 
statuses published by user_id 'dr.seuss' which took 15 ms. It was 36x faster than delete_many on a longer
string search. 

Peewee: I used delete().where and it only took 49 ms for 100 statuses. It is 11x faster than pymongo's 
delete_many but I only deleted half the same number of statuses, so really 5-6x faster. 

### Searching for one document ###
Pymongo: I used find_one to search for a user, and it took 9 ms.

Peewee: I used get and printed the result. It took less than 2 ms. Impressively fast.

### Searching for many records ###
Pymongo: I used find and count_documents() to get a count of statuses published by user_id. It took 10x longer than 
peewee. It took 215 ms. I also experimented with a larger dataset (status_updates.csv has 10x more rows, or 200k) and 
a fuzzy search with regex. It took 285 ms to find 9,912 records and 378 ms to find 47,558 records. pymongo seems to 
perform the same regardless of how large the dataset is. 

Peewee: I used a select().where.count(). It took 20 ms. It was 10x faster. I tried to do a fuzzy search on the status
dataset using select().where(table.status_text.contains(prefix)).count() and printed that count to see if the 
performance was comparable to pymongo. It took 39.77 ms to dig up 393 statuses that contained the word "happy" in a 
dataset of 200k rows. It is STILL FASTER than pymongo!

# Recommendations #

Pymongo: To optimize, I would use insert_many to load data fast, and delete_many and update_many to make changes fast.
Use regex to do fuzzy searches, which goes faster than the find method alone. 

Peewee: To optimize, I would select.where to search, update.where to update fast and delete.where to delete in bulk. 
I would also take advantage of the chunked method to load the data in batches.

In general, I would look to load the data in memory by storing it into a list, and avoid printing. Doing a count or
returning an aggregate is faster than printing results if you're looking for your function to return something.

For both peewee and pymongo, we need to make sure the fieldnames in the models and functions, and file headers match. 
I would recommend changing them in the file, as capitalizing fieldnames in code doesn't follow proper naming conventions
and requires checking that we change the fieldnames in several places in our code files, a tedious and very error-prone 
process.  

## Implementation ## 

If I were to stream data and analytics and ingest a lot of data in real-time I would use a NOSQL database like MongoDB. 
Pymongo does not discriminate against the size of the dataset, and search performs the same regardless of how big 
it is. Especially with fuzzy searches, pymongo is fast thanks to its search indexing capabilities. The data can be 
denormalized so it can go through; I can create indexes on a field, and it simply adds another column to the table 
when it doesn't recognize a field name we specified. It has shown to be less strict when adding rows, and to not require 
a key. This can eliminate some bottlenecks in the short-term if we only care to collect mass amounts of data fast and 
have it be readily available to many teams. Being largely schema-less however will cause some inconsistencies in the 
data in the long haul and can mean more cleaning up later. But for machine learning teams, who deal with mostly 
unstructured data, it won't be a problem. MongoDB would be my go-to if I had to build a monitoring system.

If I needed to write precise queries on my data, I would likely want to leverage the key constraints of SQLite. For
aggregates like count, and filtering, SQLite outperforms pymongo. You are however married to this system, so data 
integration can be a challenge. peewee is sensitive to the size of the dataset and will take 2-3x longer 
than pymongo the bigger the dataset is. So it's not great for ingesting data but would be my recommendation to data 
analysts who can slice and dice the data in their own time. If the data is related in some way, we wouldn't want to 
have to hunt down every table where the data exists, so it's to our advantage to update in one place or delete and
be alerted if it affects other tables. 
