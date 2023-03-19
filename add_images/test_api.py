from unittest import TestCase

from api import app


class ServerTest(TestCase):
    def setUp(self):
        # Special client for testing endpoints, needs to be generated from the flask object
        self.client = app.test_client()

    def test_get_users(self):
        # Execute a get request, and serialize the json into a list of dictionaries
        results = self.client.get("/users/").json
        self.assertEqual(
            results,
            [
                {
                    "email": "twinkie@mydog.com",
                    "first_name": "Twinkie",
                    "last_name": "Dog",
                    "user_id": "twinkie.dog"
                },
                {
                    "email": "mater@carsthemovie.com",
                    "first_name": "Mater",
                    "last_name": "Cars",
                    "user_id": "mater.cars"
                }
            ],
        )

    def test_lookup_user(self):
        results = self.client.get("/users/twinkie.dog").json
        self.assertEqual(
            results,
                {
                    "email": "twinkie@mydog.com",
                    "first_name": "Twinkie",
                    "last_name": "Dog",
                    "user_id": "twinkie.dog"
                },
        )

    def test_get_images(self):
        results = self.client.get("/images/").json
        self.assertEqual(
            results,
            [
                {
                    "picture_id": "0000000001",
                    "tags": "#woof ",
                    "user_id": "twinkie.dog"
                },
                {
                    "picture_id": "0000000002",
                    "tags": "#chevrolet #boomtruck ",
                    "user_id": "mater.cars"
                },
            ],
        )

    def test_lookup_image(self):
        results = self.client.get("/images/0000000002").json
        self.assertEqual(
            results,
            {
                "picture_id": "0000000002",
                "tags": "#chevrolet #boomtruck ",
                "user_id": "mater.cars"
            },
        )

    def test_get_differences(self):
        results = self.client.get("/differences/").json
        self.assertEqual(
            results,
            [
                {
                    "missing_picture_in_disk": "0000000002",
                    "user_id": "mater.cars"
                },
                {
                    "missing_picture_in_disk": "0000000001",
                    "user_id": "twinkie.dog"
                }
            ],
        )
