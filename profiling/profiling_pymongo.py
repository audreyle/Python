"""
Profiling the performance of pymongo
"""
from csv import DictReader
from time import time

from pymongo import MongoClient


def timeit(method):
    """
    Create timeit decorator to measure the performance of each function below.
    """
    def timed(*args, **kwargs):
        start = time()
        result = method(*args, **kwargs)
        end = time()
        total_time = round((end - start) * 1000, 2)
        print(f'Total time for {method.__name__} was {total_time}ms')
        return result

    return timed


# load all the data into memory by loading it into a list
with open('accounts.csv', 'r', encoding='UTF-8') as file:
    accounts = list(DictReader(file))

with open("status_updates.csv", 'r', encoding='UTF-8') as file:
    statuses = list(DictReader(file))


@timeit
def benchmark_load_one(data, table):
    """
    Load status or user data to respective table. Test insert_one.
    Store results in insert_one_user_at_a_time table.
    """
    for row in data:
        table.insert_one(row)


@timeit
def benchmark_load_many(data, table):
    """
    Load status or user data to respective table, insert_many_users
    or insert_many_statuses.
    Test first optimization using insert_many
    """
    table.insert_many(data)


# create some data to test add_row
user1 = {'_id': "dr.seuss1",
         'user_id': "dr.seuss",
         'user_name': "Theodor",
         'user_last_name': "Geisel",
         'user_email': "dr.seuss@gmail.com"}

user2 = {'_id': "dr.seuss_wife1",
         'user_id': "h.palmer.books",
         'user_name': "Helen",
         'user_last_name': "Palmer",
         'user_email': "h.palmer@hotmail.com"}

user_list = [user1, user2]

status1 = {'_id': "dr.seuss_status1",
           'status_id': "dr.seuss_00001",
           'user_id': "dr.seuss",
           'status_text': "Unless someone like you cares a whole awful lot, "
                          "nothing is going to get better."}

status2 = {'_id': "dr.seuss_wife1_status1",
           'status_id': "h.palmer.books_00001",
           'user_id': "h.palmer.books",
           'status_text': "As the old Zen saying reminds us, the finger "
                          "pointing at the moon is not the moon."}

status3 = {'_id': "dr.seuss_status2",
           'status_id': "dr.seuss_00002",
           'user_id': "dr.seuss",
           'status_text': "Think left and think right and think low and think high. "
                          "Oh, the thinks you can think up if only you try!"}

status4 = {'_id': "dr.seuss_status3",
           'status_id': "dr.seuss_00003",
           'user_id': "dr.seuss",
           'status_text': "I like nonsense; it wakes up the brain cells."}

status_list = [status1, status2, status3, status4]


@timeit
def benchmark_add_row(data, table):
    """
    Test adding one row to either insert_many_statuses or
    insert_many_users
    """
    table.insert_many(data)


@timeit
def benchmark_delete_one_user(user_id, table):
    """
    Test deleting one row in insert_many_users with delete_one
    """
    table.delete_one({'user_id': user_id})


@timeit
def benchmark_fuzzy_delete_many_users(user_name, table):
    """
    Test optimization with delete_many on records with
    user_name starting with a letter.
    """
    table.delete_many({'user_name': {'$regex': user_name}})


@timeit
def benchmark_delete_many_status(user_id, table):
    """
    Test optimization with delete_many on statuses published by
    a user_id
    """
    table.delete_many({'user_id': user_id})


@timeit
def benchmark_search_one_user(user_id, table):
    """
    Search for one record in UsersTable. Use query to search by user_id.
    """
    query = {'user_id': user_id}
    result = table.find_one(query)
    return result


@timeit
def benchmark_search_many_statuses_by_user_id(user_id, table):
    """
    Search for multiple records in StatusTable by the user_id and print a count.
    """
    count = table.count_documents({'user_id': user_id})
    print(count)
    return table.find({'user_id': user_id})


@timeit
def benchmark_fuzzy_search_many_users_by_name(user_name, table):
    """
    Search for many users whose user_name starts with a letter and print a count.
    """
    count = table.count_documents({'user_name': {'$regex': user_name}})
    print(count)
    return table.find({'user_name': {'$regex': user_name}})


@timeit
def benchmark_fuzzy_search_many_statuses_by_user_id(user_id, table):
    """
    Search for many statuses whose text contains a word and print a count.
    """
    count = table.count_documents({'user_id': {'$regex': user_id}})
    print(count)
    return table.find({'user_id': {'$regex': user_id}})


# def print_status(status):
#     print(f'{status["status_id"]}')

@timeit
def benchmark_update_one_user(user_id, user_name, user_last_name, email, table):
    """
    Update one record with update_one
    """
    query = {"user_id": user_id}
    new_data = {"user_name": user_name, "user_last_name": user_last_name, 'user_email': email}
    table.update_one(query, {"$set": new_data})


@timeit
def benchmark_update_many_statuses(user_id, table):
    """
    Update many records with update_many. Filter all statuses
    by this user_id and replace status_text with "Who-ville"
    """
    table.update_many(
        {'user_id': user_id},
        {"$set":
            {
                "status_text": "Who-Ville"
            }}
    )


mongo = MongoClient()
insert_one_table = mongo.Benchmark['insert_one_user_at_a_time']
# benchmark_load_one(accounts, insert_one_table)

insert_many_table = mongo.Benchmark['insert_many_users']
# benchmark_load_many(accounts, insert_many_table)


# benchmark_add_row(user_list, insert_many_table)
# benchmark_delete_one_user("h.palmer.books", insert_many_table)
# benchmark_update_one_user("dr.seuss", "Theodor", "Geisel", "dr.seuss@gmail.com",
# insert_many_table)
# benchmark_search_one_user("dr.seuss", insert_many_table)

status_many_table = mongo.Benchmark["insert_many_statuses"]
# benchmark_load_many(statuses, status_many_table)
# benchmark_add_row(status_list, status_many_table)
# benchmark_search_many_statuses_by_user_id("Jaclyn.Lola99", status_many_table)
# benchmark_delete_many_status("dr.seuss", status_many_table)
# benchmark_update_many_statuses("Jaclyn.Lola99", status_many_table)
# benchmark_search_many_statuses_by_user_id("Jasmina.Obie49", status_many_table)
# benchmark_delete_many_status("Jasmina.Obie49", status_many_table)

# benchmark_fuzzy_search_many_users_by_name("A", insert_many_table)
# benchmark_fuzzy_delete_many_users("A", insert_many_table)
# benchmark_fuzzy_search_many_statuses_by_user_id("De", status_many_table)

# mongo.close()
