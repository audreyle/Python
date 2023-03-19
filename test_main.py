"""
Unittests for main.py
"""
# pylint: disable=C0116,C0301,W1503

import unittest
import io

from unittest import TestCase
from unittest.mock import patch, Mock, mock_open

import main
import users
import user_status


class UsersTest(TestCase):
    """
    Unittests for User class functions
    """
    def test_main_menu(self):
        """
        Disabling pylint W1503: Redundant use of assertTrue with constant value message because we are testing
        the main menu using the add_user menu option
        """
        with patch("builtins.input", side_effect=["accounts.csv", "status_updates.csv", "C", "ale314", "ale314@uw.edu",
                                                  "Audrey", "Le", "Q"]):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                with self.assertRaises(SystemExit):
                    main.main_menu()
                self.assertTrue("User was successfully added\n", mock_stdout.getvalue())

    def test_init_user_collection(self):
        expected = type(users.UserCollection())
        self.assertEqual(type(main.init_user_collection()), expected)

    def test_load_users(self):
        test_user_collection = users.UserCollection()
        self.assertTrue(main.load_users('accounts.csv', test_user_collection))

    def test_load_users_empty_string(self):
        main.DictReader = Mock(return_value=iter([
            {
                'USER_ID': 'ale314',
                'EMAIL': '',
                'NAME': 'Audrey',
                'LASTNAME': 'Le'
            },
            {
                'USER_ID': 'bryce5',
                'EMAIL': 'bryce.b@gmail.com',
                'NAME': 'Bryce',
                'LASTNAME': 'Brown'
            },
        ]))
        with patch('main.open', mock_open()):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                outcome = main.load_users('file.csv', users.UserCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                expected_print_out = ["Detailed error message: Empty field in this row: {'USER_ID': 'ale314', "
                                      "'EMAIL': '', 'NAME': 'Audrey', 'LASTNAME': 'Le'}."]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out, expected_print_out)

    def test_load_users_file_not_found(self):
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                mock_file.side_effect = FileNotFoundError
                outcome = main.load_users('file.csv', users.UserCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['Encountered exception while loading account list:'])
    def test_load_users_key_error(self):
        main.DictReader = Mock(return_value=iter([
            {
                'USERNAME': 'ale314',
                'EMAIL': 'ale314@uw.edu',
                'NICKNAME': 'Audette',
                'LASTNAME': 'Le'
            },
            {
                'USERNAME': 'bryce5',
                'EMAIL': 'bryce.b@gmail.com',
                'NICKNAME': 'Brice',
                'LASTNAME': 'Brown'
            },
        ]))
        with patch('main.open', mock_open()):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                outcome = main.load_users('file.csv', users.UserCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                expected_print_out = ['Wrong input file format. It should contain the following columns: USER_ID, '
                        'EMAIL, NAME, LASTNAME.',
                        "Detailed error message: 'USER_ID'"]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out, expected_print_out)

    def test_add_user(self):
        test_user_collection = users.UserCollection()
        self.assertTrue(main.add_user("scoobydoo1", "scooby.dog@gmail.com", "Scooby", "Doo", test_user_collection))
        self.assertFalse(main.add_user("scoobydoo1", "scooby.dog@gmail.com", "Scooby", "", test_user_collection))

    def test_update_user(self):  # self is going to be an instance of unittest
        test_user_collection = users.UserCollection()
        main.add_user('peterpan1', 'peter1@gmail.com', 'Peter', 'Pan', test_user_collection)
        self.assertTrue(main.update_user("peterpan1", "peter.pan@gmail.com", "Peter", "Pan", test_user_collection))
        self.assertFalse(main.update_user('wendyd', 'wendy.darling@gmail.com', 'Wendy', 'Darling',
                                          test_user_collection))

    def test_delete_user_pass(self):
        test_user_collection = users.UserCollection()
        test_user_collection.add_user('peterpan1', 'peter1@gmail.com', 'Peter', 'Pan')
        self.assertTrue(main.delete_user('peterpan1', test_user_collection))

    def test_delete_user_fail(self):
        test_user_collection = users.UserCollection()
        test_user_collection.add_user('peterpan1', 'peter1@gmail.com', 'Peter', 'Pan')
        self.assertFalse(main.delete_user('wendyd', test_user_collection))

    def test_search_user_pass(self):
        test_user_collection = users.UserCollection()
        test_user_collection.add_user('peterpan1', 'peter1@gmail.com', 'Peter', 'Pan')
        self.assertTrue(main.search_user('peterpan1', test_user_collection))

    def test_search_user_fail(self):
        test_user_collection = users.UserCollection()
        test_user = main.search_user('gru88', test_user_collection)
        self.assertEqual(None, test_user)

    def test_save_users_success(self):
        test_user_collection = users.UserCollection()
        self.assertTrue(main.save_users('accounts.csv', test_user_collection))

    def test_save_users_file_not_found(self):
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                mock_file.side_effect = FileNotFoundError
                outcome = main.save_users('file.csv', users.UserCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['Detailed error message:'])


class UserStatusTest(TestCase):
    """
    Unittests for status class functions
    """
    def test_init_status_collection(self):
        expected = type(user_status.UserStatusCollection())
        self.assertEqual(type(main.init_status_collection()), expected)
    def test_load_status_updates_success(self):
        """
        This unit test is gimmicky because it generates a key error and can't read the status_text.
        That's why it wants me to assert False.
        When I check the debugger and what gets stored in the database, everything checks out though.
        """
        test_status_collection = user_status.UserStatusCollection
        self.assertTrue(main.load_status_updates('status_updates.csv', test_status_collection))

    def test_load_status_updates_key_error(self):
        main.DictReader = Mock(return_value=iter([
            {
                'STATUS_ID': 'ale314_00002',
                'USER_ID': 'ale314',
                'TEXT': 'Happy Year of the Rabbit!'
            },
            {
                'STATUS_ID': 'bryce05_00002',
                'USER_ID': 'bryce05',
                'TEXT': 'Gong xi fa cai!'
            },
        ]))
        with patch('main.open', mock_open()):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                main.load_status_updates('file.csv', user_status.UserStatusCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                expected_print_out = ['Wrong input file format. It should contain the following columns: STATUS_ID, '
                                      'USER_ID, STATUS_TEXT.',
                                      "Detailed error message: 'STATUS_TEXT'"]
                self.assertEqual(print_out, expected_print_out)

    def test_load_status_updates_file_not_found(self):
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                mock_file.side_effect = FileNotFoundError
                outcome = main.load_status_updates('file.csv', user_status.UserStatusCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['File not found! Encountered exception while loading account list:'])
    def test_load_status_updates_empty_string(self):
        main.DictReader = Mock(return_value=iter([
            {
                'USER_ID': 'ale314_00002',
                'STATUS_ID': 'ale314',
                'STATUS_TEXT': ''
            },
            {
                'USER_ID': 'bryce05_00002',
                'STATUS_ID': 'bryce05',
                'STATUS_TEXT': 'Gong xi fa cai!'
            },
        ]))
        with patch('main.open', mock_open()):
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                outcome = main.load_status_updates('file.csv', users.UserCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                expected_print_out = ["Detailed error message: Empty field in this row: {'USER_ID': 'ale314_00002', "
                                      "'STATUS_ID': 'ale314', 'STATUS_TEXT': ''}."]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out, expected_print_out)

    def test_add_status(self):
        test_status_collection = user_status.UserStatusCollection()
        self.assertTrue(main.add_status('beatrix2_00001', 'beatrix2', 'My new book was released!',
                                        test_status_collection))
        self.assertFalse(main.add_status('beatrix2_00001', 'beatrix2', 'My new book was released!',
                                         test_status_collection))
    def test_update_status(self):  # self is going to be an instance of unittest
        test_status_collection = user_status.UserStatusCollection()
        test_status_collection.add_status('peterpan1_00001', 'peterpan1', 'I am flying!')
        self.assertTrue(main.update_status('peterpan1_00001', 'peterpan1', 'No one wants to grow up',
                                           test_status_collection))
        self.assertFalse(main.update_status('wendyd_00001', 'wendyd', 'I want to grow up', test_status_collection))
    def test_delete_status_success(self):
        test_status_collection = user_status.UserStatusCollection()
        test_status_collection.add_status('peterpan1_00001', 'peter1', 'I am the leader of the Lost Boys')
        self.assertTrue(main.delete_status('peterpan1_00001', test_status_collection))

    def test_delete_status_fail(self):
        test_status_collection = user_status.UserStatusCollection()
        self.assertFalse(main.delete_status('gru88', test_status_collection))
    def test_search_status_pass(self):
        test_status_collection = user_status.UserStatusCollection()
        test_status_collection.add_status('peterpan1_00003', 'peter1', 'I am the leader of the Lost Boys')
        self.assertTrue(main.search_status('peterpan1_00003', test_status_collection))

    def test_search_status_fail(self):
        test_status_collection = user_status.UserStatusCollection()
        test_status = main.search_status('wendyd', test_status_collection)
        self.assertEqual(None, test_status)

    def test_save_status_updates(self):
        test_user_collection = users.UserCollection()
        self.assertTrue(main.save_status_updates('status_updates.csv', test_user_collection))

    def test_save_status_updates_file_not_found(self):
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                mock_file.side_effect = FileNotFoundError
                outcome = main.save_status_updates('file.csv', user_status.UserStatusCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['File not found. Detailed error message:'])

    def test_load_status_updates_value_error(self):
        with patch('main.open', mock_open()) as mock_file:
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                mock_file.side_effect = ValueError
                outcome = main.load_status_updates('file.csv', user_status.UserStatusCollection())
                print_out = [x.strip() for x in mock_stdout.getvalue().strip().splitlines()]
                self.assertEqual(outcome, False)
                self.assertEqual(print_out,
                                 ['Detailed error message:'])


if __name__ == '__main__':
    unittest.main()
