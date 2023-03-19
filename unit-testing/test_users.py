"""
Unit testing methods in User class
"""
from unittest import TestCase

from peewee import SqliteDatabase
from socialnetwork_model import UsersTable
from users import UserCollection


class TestUserCollection(TestCase):
    """
    Creating a test User class for testing methods in User class
    """
    def setUp(self):
        """
        Create a mock database to avoid using users.db during testing
        """
        # Don't use a real database, instead, let's use an in-memory version that
        # gets thrown away once tests are done
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        # Bind our UsersTable to this one test database instead of our users.db file
        self.database.bind([UsersTable])
        # Connect and create tables using the data model for UsersTable
        self.database.connect()
        self.database.create_tables([UsersTable])
        # Seeding data
        self.user_collection = UserCollection(self.database)
        self.user_collection.add_user("ale314", "Audrey", "Le", "ale314@uw.edu")
        self.user_collection.add_user("bryce05", "Bryce", "Brown", "bryce05@gmail.com")

    def tearDown(self):
        """
        Disconnect test databases
        """
        self.database.drop_tables([UsersTable])
        self.database.close()

    def test_add_user_success(self):
        """
        Testing add_user in users.py
        """
        user_id = "jerry.tom1"
        user_name = "Jerry"
        user_last_name = "Mouse"
        email = "jerry.tom1@gmail.com"
        self.assertTrue(
            self.user_collection.add_user(user_id, user_name, user_last_name, email)
        )

    def test_add_user_conflict(self):
        """
        Testing add_user in users.py when the user already exists
        """
        user_id = "ale314"
        user_name = "Audrey"
        user_last_name = "Le"
        email = "ale314@uw.edu"
        self.assertFalse(
            self.user_collection.add_user(user_id, user_name, user_last_name, email)
        )

    def test_search_user_success(self):
        """
        Testing search_user in users.py
        """
        self.assertTrue(self.user_collection.search_user("bryce05"))

    def test_search_user_fail(self):
        """
        Testing how search_user in users.py fails
        """
        self.assertFalse(self.user_collection.search_user("dr.seuss1"))

    def test_delete_user_success(self):
        """
        Testing delete_user in users.py
        """
        self.assertTrue(self.user_collection.delete_user("bryce05"))

    def test_delete_user_fail(self):
        """
        Testing how delete_user in users.py fails
        """
        self.assertFalse(self.user_collection.delete_user("bryce03"))

    def test_update_email_success(self):
        """
        Testing update_email in users.py
        """
        self.assertTrue(self.user_collection.update_email("ale314", "audrey314.le@gmail.com"))

    def test_update_email_fail(self):
        """
        Testing how update_email in users.py fails
        """
        self.assertFalse(self.user_collection.update_email("strumpf", "strumpf@gmail.com"))
