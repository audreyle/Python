# pylint: disable=C0103,W0611
"""
Profiling the performance of Peewee
Make sure to run peewee_model.py first!
"""

from csv import DictReader

from peewee import chunked

from peewee_model import database, StatusTable, UsersTable
from profiling_pymongo import timeit

# load all the data into memory by loading it into a list
with open('accounts.csv', 'r', encoding='UTF-8') as file:
    accounts = list(DictReader(file))

with open("status_updates.csv", 'r', encoding='UTF-8') as file:
    statuses = list(DictReader(file))


@timeit
def benchmark_add_user(user_id, user_name, user_last_name, user_email, table):
    """
    Add a row to UsersTable and save.
    """
    result = table.create(
        user_id=user_id,
        user_name=user_name,
        user_last_name=user_last_name,
        user_email=user_email
    )
    result.save()


@timeit
def benchmark_add_status(status_id, user_id, status_text, table):
    """
    I had to create a separate function to add a status because SQLite forces me
    to create a key.
    """
    result = table.create(
        status_id=status_id,
        user_id=user_id,
        status_text=status_text
    )
    result.save()


@timeit
def benchmark_update_one_user(user_id, user_name, user_last_name, user_email, table):
    """
    I prefer to create a separate function to test the performance of
    adding one row, in this case, one user which needs a distinct set of
    parameters.
    """
    result = table.get(table.user_id == user_id)
    result.user_name = user_name
    result.user_last_name = user_last_name
    result.user_email = user_email
    result.save()


@timeit
def benchmark_update_many_statuses(user_id, status_text, table):
    """
    Update in bulk
    """
    query = table.update(status_text=status_text).where(table.user_id == user_id)
    query.execute()


@timeit
def benchmark_delete_one_user(user_id, table):
    """
    I was tempted to create a function to delete both user and statuses.
    You'd essentially delete everything associated with the user_id, but
    for it to work, you'd still need to call it twice, and specify which
    table.
    """
    result = table.get(table.user_id == user_id)
    result.delete_instance()


@timeit
def benchmark_delete_many_statuses(user_id, table):
    """
    Delete multiple records where user_id matches
    """
    query = table.delete().where(table.user_id == user_id)
    query.execute()


@timeit
def benchmark_search_one_user(user_id, table):
    """
    Search for one row and print all its fields
    """
    result = table.get(table.user_id == user_id)
    print(result.user_name, result.user_last_name, result.user_email)


@timeit
def benchmark_search_many_statuses_by_user_id(user_id, table):
    """
    Search multiple records and print primary key
    Counts how many statuses the query found by the status_id and prints count.
    """
    # for status in table.select(table.status_id).where(table.user_id == user_id):
    #     print(status)
    count = table.select().where(table.user_id == user_id).count()
    print(count)


@timeit
def benchmark_fuzzy_search_status(prefix, table):
    """
    Fuzzy search for statuses that contain the word and print a count.
    """
    # for result in table.select().where(table.status_text.contains(prefix)):
    #     print(result.status_text)
    count = table.select().where(table.status_text.contains(prefix)).count()
    print(count)


@timeit
def benchmark_load_one(data, uc):
    """
    I tried this first, because I did not want to mess with the headers.
    In order for this to work, we need to instantiate a user collection.
    """
    for row in data:
        uc.add_user(
            row['user_id'],
            row['user_name'],
            row['user_last_name'],
            row['user_email']
        )


@timeit
def benchmark_load_many(data, table):
    """
    This can be used to load ANY file, and is key-agnostic
    so long as you created the fields in peewee_model and the
    headers of your file match these fieldnames in peewee_model.py
    """
    with database.atomic():
        for batch in chunked(data, 100):
            table.insert_many(batch).execute()


# uc = UserCollection(database)
# benchmark_load_one(accounts, uc)
# benchmark_load_many(accounts, UsersTable)
# benchmark_load_many(statuses, StatusTable)

# benchmark_add_user("ale314", "Audrey", "Le", "ale314@uw.edu", UsersTable)
# benchmark_search_one_user("Bria.Sidonie50", UsersTable)
# benchmark_update_one_user("ale314", "Audrey", "Le", "audrey314.le@gmail.com")
# benchmark_update_one_user("Brittaney.Gentry86", "Britney", "Gentry",
# "Brittaney.Gentry86@hotmail.com", UsersTable)
# benchmark_delete_one_user("Gaye.Arno57", UsersTable)

# benchmark_search_many_statuses_by_user_id('Roshelle.Pironi69', StatusTable)
# benchmark_update_many_statuses("Nadiya.Pappas68", "I am Nadiya", StatusTable)
# benchmark_search_many_statuses_by_user_id('Nadiya.Pappas68', StatusTable)
# benchmark_delete_many_statuses('Jasmina.Obie49', StatusTable)

# benchmark_fuzzy_search_status("happy", StatusTable)
# benchmark_add_user("dr.seuss", "Theodor", "Geisel", "dr.seuss@gmail.com", UsersTable)
# benchmark_add_status("dr.seuss_00001", "dr.seuss",
#                      "Unless someone like you cares a whole awful lot, nothing "
#                      "is going to get better.", StatusTable)
