# Performance report on pandas_chunks.py and load_status_queue.py #

## Pandas_chunks.py ## 
Pandas_chunks.py does not assign different chunks to different queues, which is the focus of
load_status_queue.py. 

Pandas_chunks.py compares the performance of a single process, joined processes and
multiple workers (Process vs. ProcessPoolExecutor on 2, 5, 10 workers). On 1, 5, 10
and 50 pieces of work. Adding 2k vs 200k rows of data. 

## Performance of load_users() which prints 2k rows in chunks of 10 ##

| Tasks | Processes | Process_pool | Max_Workers     |
|-------|-----------|--------------|-----------------|
| 50    | 26.87s    | 16.83s       | 5 (cpu = 4)     |
| 5     | 2.76s     | 2.95s, 2.96s | 5, 10 (cpu = 4) |
| 5     |           | 4.02s        | 1 (cpu = 4)     |
| 2     | 1.35s     | 1.37s        | 2 (cpu = 4)     |
| 1     | 1.22s     | 1.09s        | 2               |


## Performance of load_status() which prints 200k rows in chunks of 1000 ##
I would've made load_status comparable to load_user but a chunk size of 10 for that large of a dataset
would have been a long coffee break!

| Tasks | Processes  | Process_pool  | Max_Workers     |
|-------|------------|---------------|-----------------|
| 50    | 5 1/2 mins | 7 mins        | 5 (cpu = 4)     |
| 5     | 41.25s     | 38.8s, 39.03s | 5, 10 (cpu = 4) |
| 5     |            | 60.88s        | 1 (cpu = 4)     |
| 2     | 16.85s     | 16.71s        | 2 (cpu = 4)     |
| 1     | 13.66s     | 12.69s        | 2               |

## Performance of adding 2K rows to UsersTable with insert_one ##
| Tasks | Processes  | Process_pool | Max_Workers |
|-------|------------|--------------|-------------|
|  1    |   2.12s    | 2.15s        | 2           |

## Performance of adding 200K rows to StatusTable with insert_one ##

| Tasks | Processes | Process_pool | Max_Workers |
|-------|-----------|--------------|-------------|
|  1    | 2.2 mins  | 2 mins       | 2           |


## Performance of adding 2K rows to UsersTable with insert_many ##
| Tasks | Processes | Process_pool | Max_Workers |
|-------|-----------|--------------|-------------|
|  1    | 1.61s     | 1.58s        | 2           |


## Performance of adding 200K rows to StatusTable with insert_many ##
I did not see too much of a difference between 1 process and 2 workers 
when each was asked to import the status_updates.csv to mongoDB 5x, resulting
in 1M records.

| Tasks           | Processes | Process_pool | Max_Workers |
|-----------------|-----------|--------------|-------------|
| 1   200k rows   | 6.22s     | 6.71s        | 2           |
| 5   1M records  | 13.66s    | 16.95s       | 2           |
| 10  2M records  | 25.83s    | 31.7s        | 2           |
| 10              |           | 29s          | 5           |
| 10              |           | 29.9s        | 3           |
| 10              |           | 27.64s       | 10          |
| 10              |           | 30.06s       | 8           |
| 50  10M records | 3mins 10s | 2 mins 20s   | 5           |


My cores were not happy when I assigned 5 workers to add 2M records. The fan
started running, and it also did not lead to any significant performance gains from 2 workers. 
Doubling the number of workers helped by a couple seconds. 

When adding 10M records, I saw a 50-second advantage to using 5 workers. 

## Conclusions ##

All in all, because I only have 2 cores (or 4 cpus) I don't see too much difference in letting
an executor pool processes.

Because we don't care whether we have replicas of the data in our database (we should, but it
doesn't make sense when mongoDB is the source of truth) it doesn't matter too much whether I 
have 2 workers to add 200k status updates. The advantage came from chunking in sizes of 1000
rows and using insert_many. It took 2 minutes with 2 workers when using insert_one, and less than 
7 seconds with insert_many. The performances between 1 process and 2 workers were comparable.

When adding in smaller chunks (10 accounts at a time), you do see performance gains printing 100K
accounts when you process pool with 5 workers. I conclude that chunksize using pandas is also a 
major factor in improving performance.

## Load_status_queue.py
Load_status_queue.py assigns different chunks of data to different queue, which starts a separate
process for each queue that calls add_status.py to get the results from the queue that is passed,
in this case a list of dictionaries, and insert_one(chunk) to the StatusTable.

| Chunksize | Processes | Time    | Method     |
|-----------|-----------|---------|------------|
| 10,000    | 2         | 144s    | insert_one |
| 1,000     | 2         | 159.22s | insert_one |
| 10,000    | 5         | 157s    | insert_one |



### Conclusions ###

For add_status() in load_status_queue.py I was limited to insert_one because the chunk I am passing
is a list. The fan started running when I reduced the chunksize to 1,000 but it only added another 15s
to the job. Queueing up chunks of data and allocating them to different processes did not make a 
difference. It still took 2 mins. 


