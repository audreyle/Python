from pathlib import Path

from peewee import IntegrityError, SqliteDatabase, DoubleField, CharField, Model, ForeignKeyField
from playhouse.dataset import DataSet



class DataTables:

    def __init__(self, file_name='user.db', database=None):
        self.file_name = file_name
        self.database = database

    def __enter__(self):
        self.database = SqliteDatabase(self.file_name, pragmas={"foreign_keys": 1})
        self.database.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()
        if exc_type == IntegrityError:
            # We'll print an error, but leave the exception unhandled
            print("An error has occurred")
            return False


class UserTable(Model):
    class Meta:
        database = DataTables().__enter__().database

    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    email = CharField(max_length=32)


class StatusTable(Model):
    class Meta:
        database = DataTables().__enter__().database

    status_id = CharField(primary_key=True, max_length=32)
    user_id = ForeignKeyField(UserTable, backref="UserTable", on_delete="CASCADE")
    status_text = CharField(max_length=32)

class PictureTable(Model):
    class Meta:
        database = DataTables().__enter__().database

    picture_id = CharField(primary_key=True, max_length=32)
    user_id = ForeignKeyField(UserTable, backref="UserTable", on_delete="CASCADE")
    tags = CharField(max_length=100)

class DifferenceTable(Model):
    class Meta:
        database = DataTables().__enter__().database

    missing_picture_in_disk = CharField(primary_key=True, max_length=32)
    user_id = ForeignKeyField(UserTable, backref="UserTable", on_delete="CASCADE")


with DataTables('user.db') as dt:
    dt.database.create_tables(([UserTable, StatusTable, PictureTable, DifferenceTable]))
    ds = DataSet(dt.database)
    userstable = ds["usertable"]
    #userstable.delete()
    statustable = ds["statustable"]
    #statustable.delete()
    picturetable = ds["picturetable"]
    #picturetable.delete()
    differences_table = ds["differencetable"]
    #differences_table.delete()
    # dt.database.close()


