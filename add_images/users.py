'''
Classes for user information for the social network project
'''
# pylint: disable=R0903
import logging
from datetime import datetime
from peewee import IntegrityError, DoesNotExist
from socialnetwork_model import userstable


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
)
file_handler = logging.FileHandler(
    filename=f"logging_{datetime.now():%Y_%m_%d}.log"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)




def add_user(user_id, email, user_name, user_last_name):
    """
    Adds a new user to the collection
    """
    try:
        userstable.insert(user_id=user_id, user_name=user_name, user_last_name=user_last_name,
                          email=email)
        logger.info('New user added')
        return True
    except IntegrityError:
        logger.error('An error occurred')
        return False


def delete_user(user_id):
    """
    Deletes an existing user
    """
    try:
        userstable.delete(user_id=user_id)
        return True
    # Catches any errors not finding this record
    except DoesNotExist:
        logger.error('An error has occurred when deleting a user')
        return False


def modify_user(user_id, email, user_name, user_last_name):
    """
    Modifies an existing user
    """
    try:
        userstable.update(user_id=user_id, user_name=user_name, user_last_name=user_last_name,
                          email=email, columns=['user_id'])

        return True
    # Catches any errors not finding this record
    except DoesNotExist:
        return False


def search_user(user_id):
    """
    Searches for user data
    """
    try:
        result = userstable.find_one(user_id=user_id)
        return result
    # Catches any errors not finding this record
    except DoesNotExist:
        return None
