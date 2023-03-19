import io
from unittest import TestCase
from unittest.mock import MagicMock, patch

from main import add_user, search_user, delete_user, update_email, add_status, search_status, delete_status, \
    update_status


class TestMain(TestCase):
    def test_add_user_success(self):
        # Leveraging MagicMock instead of User
        mock_user = MagicMock()
        # Setting values to pre-seeded data
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        user_collection = MagicMock()
        # Change the return value of add_user() to our now mocked user
        user_collection.add_user.return_value = mock_user
        with patch("builtins.input", side_effect=["serena.tennis", "Serena", "Williams", "serena.tennis@gmail.com"]):
            # calling add_user on our mocked user_collection
            new_user = add_user(user_collection)
            self.assertEqual(new_user, mock_user)
            # Verify our mocked method was called with these 4 values
            user_collection.add_user.assert_called_with("serena.tennis", "Serena", "Williams",
                                                        "serena.tennis@gmail.com")

    def test_search_user_success(self):
        # Leveraging MagicMock instead of User
        mock_user = MagicMock()
        # Setting values to pre-seeded data
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        user_collection = MagicMock()
        user_collection.add_user.return_value = mock_user
        # Change the return value of search_user() to our now mocked user
        user_collection.search_user.return_value = mock_user
        with patch("builtins.input", side_effect=["serena.tennis"]):
            # calling search_user on our mocked user_collection
            search_user(user_collection)
            # Verify that a result was returned. It is a magicMock object
            self.assertIsNotNone(user_collection.search_user.return_value)
            # Verify our mocked method was called with "serena.tennis"
            user_collection.search_user.assert_called_with("serena.tennis")

    def test_search_user_not_found(self):
        with (
            patch("builtins.input", side_effect=["serena.williams"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            # Leveraging MagicMock instead of User
            user_collection = MagicMock()
            # Change the return value of search_user() to None, signaling that user is not found
            user_collection.search_user.return_value = None
            # calling search_user on our mocked user_collection
            search_user(user_collection)
            # Verify print statement on user client
            self.assertEqual(mock_stdout.getvalue().strip(), "serena.williams was not found")
            # Verify the mocked method was called with "serena.williams"
            user_collection.search_user.assert_called_with("serena.williams")

    def test_delete_user_success(self):
        with (
            patch("builtins.input", side_effect=["scoobydoo1"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            # Leveraging MagicMock instead of User
            mock_person = MagicMock()
            # Setting values to pre-seeded data
            mock_person.user_id = "scoobydoo1"
            mock_person.email = "scoobydoo1@yahoo.com"
            mock_person.user_name = "Scooby"
            mock_person.user_last_name = "Doo"
            user_collection = MagicMock()
            # Change the return value of search_user() to our now mocked user
            user_collection.add_user.return_value = mock_person
            # calling delete_user on our mocked user_collection
            delete_user(user_collection)
            # Verify print statement
            self.assertEqual(
                mock_stdout.getvalue().strip(),
                "Removed scoobydoo1",
            )
            # verify our mocked method was called with "scoobydoo1"
            user_collection.delete_user.assert_called_with("scoobydoo1")

    def test_delete_user_fail(self):
        with (
            patch("builtins.input", side_effect=["shaggy1"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            # Leveraging MagicMock instead of User
            user_collection = MagicMock()
            # Change the return value of delete_user() to None, signaling that user is not found
            user_collection.search_user.return_value = None
            # calling delete_user on our mocked user_collection
            search_user(user_collection)
            # Verify print statement on user client
            self.assertEqual(mock_stdout.getvalue().strip(), "shaggy1 was not found")
            # Verify the mocked method was called with "shaggy1"
            user_collection.search_user.assert_called_with("shaggy1")

    def test_update_email_success(self):
        with (
            patch("builtins.input", side_effect=["serena.tennis", "serena.williams@outlook.com"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            # Leveraging MagicMock instead of User
            mock_user = MagicMock()
            # Setting values to pre-seeded data
            mock_user.user_id = "serena.tennis"
            mock_user.user_name = "Serena"
            mock_user.user_last_name = "Williams"
            mock_user.email = "serena.tennis@gmail.com"
            user_collection = MagicMock()
            # Change the return value of add_user() to our now mocked user
            user_collection.add_user.return_value = mock_user
            # calling update_email on our mocked user_collection
            update_email(user_collection)
            # Verify print statement on user client
            self.assertEqual(mock_stdout.getvalue().strip(), "serena.tennis's new email is now "
                                                             "serena.williams@outlook.com")
            # Verify our mocked method was called with these values
            user_collection.update_email.assert_called_with("serena.tennis", "serena.williams@outlook.com")

    def test_update_email_fail(self):
        with (
            patch("builtins.input", side_effect=["shaggy1", "shaggy.doo@gmail.com"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            # Leveraging MagicMock instead of User
            user_collection = MagicMock()
            mock_user = MagicMock()
            # Change the return value of update_email to None, signaling that user_id was not found
            user_collection.update_email.return_value = None
            # calling update_email on our mocked user_collection
            update_email(user_collection)
            # Verify print statement on user client
            self.assertEqual(mock_stdout.getvalue().strip(), "Failed to update to shaggy.doo@gmail.com")
            # Verify the mocked method was called with this non-existent user credentials
            user_collection.update_email.assert_called_with("shaggy1", "shaggy.doo@gmail.com")

    def test_add_status_success(self):
        # Leveraging MagicMock instead of User
        mock_user = MagicMock()
        # Setting values to pre-seeded data. Add user first.
        mock_user.user_id = "serena.tennis"
        mock_user.user_name = "Serena"
        mock_user.user_last_name = "Williams"
        mock_user.email = "serena.tennis@gmail.com"
        user_collection = MagicMock()
        # Now mock status
        user_collection.add_user.return_value = mock_user
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "serena.tennis_00001"
        mock_status.user_id = "serena.tennis"
        mock_status.status_text = "I don't like to lose"
        # Change the return value of add_status to our mocked status
        status_collection.add_status.return_value = mock_status
        with patch("builtins.input", side_effect=["serena.tennis_00001", "serena.tennis",
                                                  "I don't like to lose"]):
            # calling add_status on our mocked status_collection
            new_status = add_status(status_collection)
            self.assertEqual(new_status, mock_status)
            # Verify our mocked method was called with these 3 values
            status_collection.add_status.assert_called_with("serena.tennis_00001", "serena.tennis",
                                                            "I don't like to lose")

    def test_search_status_success(self):
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "serena.tennis_00001"
        # Hard code user_id, so we don't have to mock user as well.
        mock_status.user_id = "serena.tennis"
        mock_status.status_text = "I don't like to lose"
        # Change the return value of search_status() to our now mocked status
        status_collection.search_status.return_value = mock_status
        with (
            patch("builtins.input", side_effect=["serena.tennis"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            # calling search_status on our mocked status_collection
            search_status(status_collection)
            # Verify that a result was returned. It is a magicMock object
            self.assertIsNotNone(status_collection.search_status.return_value)
            self.assertEqual(mock_stdout.getvalue().strip(), "serena.tennis_00001 from serena.tennis has status(es): "
                                                             "I don't like to lose.")
            # Verify our mocked method was called with user_id "serena.tennis"
            status_collection.search_status.assert_called_with("serena.tennis")

    def test_search_status_not_found(self):
        with (
            patch("builtins.input", side_effect=["serena.tennis_00003"]),
            patch("sys.stdout", new_callable=io.StringIO) as mock_stdout,
        ):
            status_collection = MagicMock()
            # Change the return value of search_status() to None, signaling that status_id was not found
            status_collection.search_status.return_value = None
            # calling search_status on our mocked user_collection
            search_status(status_collection)
            # Verify print statement on user client
            self.assertIsNone(status_collection.search_status.return_value)
            self.assertEqual(mock_stdout.getvalue().strip(), "serena.tennis_00003 was not found")
            # Verify the mocked method was called with "serena.williams"
            status_collection.search_status.assert_called_with("serena.tennis_00003")

    def test_delete_status_success(self):
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "serena.tennis_00002"
        # Hard code user_id, so we don't have to mock user as well.
        mock_status.user_id = "serena.tennis"
        mock_status.status_text = "You have to believe in yourself when no one else does."
        # Change the return value of delete_status() to our now mocked status, so we have
        # a status object to delete with delete_status
        status_collection.delete_status.return_value = mock_status
        with patch("builtins.input", side_effect=["serena.tennis_00002"]):
            # calling search_status on our mocked status_collection
            delete_status(status_collection)
            # Verify that there was an object to delete
            self.assertIsNotNone(status_collection.delete_status.return_value)
            # Verify our mocked method was called with user_id "serena.tennis"
            status_collection.delete_status.assert_called_with("serena.tennis_00002")

    def test_update_status_success(self):
        mock_status = MagicMock()
        status_collection = MagicMock()
        mock_status.status_id = "madonna_lyrics_00001"
        # Hard coding Madonna's user_id to avoid mocking up user as well
        mock_status.user_id = "madonna_lyrics"
        mock_status.status_text = "You're frozen when your heart's not open"
        status_collection.add_status.return_value = mock_status
        with patch("builtins.input", side_effect=["madonna_lyrics_00001", "La Isla Bonita"]):
            # calling search_status on our mocked status_collection
            update_status(status_collection)
            # Verify that a result was returned. It is a magicMock object
            self.assertIsNotNone(status_collection.update_status.return_value)
