'''
classes to manage the user status messages
'''
# pylint: disable=R0903
import logging
from datetime import datetime
from peewee import IntegrityError, DoesNotExist
from socialnetwork_model import statustable


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


class UserStatus:
    """
    class to hold status message data
    """

    def __init__(self, status_id, user_id, status_text):
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text
        logger.info('New user status instance created')


def add_status(status_id, user_id, status_text):
    """
    add a new status message to the collection
    """
    try:
        statustable.insert(status_id=status_id, user_id=user_id, status_text=status_text)
        logger.info('New status added')
        return True
    except IntegrityError:
        logger.error('An error occurred when adding a user')
        return False


def modify_status(status_id, user_id, status_text):
    """
    Modifies a status message

    The new user_id and status_text are assigned to the existing message
    """
    try:
        statustable.update(status_id=status_id, user_id=user_id, status_text=status_text,
                           columns=['status_id'])
        logger.info('User status updated')
        return True
    # Catches any errors not finding this record
    except IntegrityError:
        logger.error('Unable to update user status')
        return False


def delete_status(status_id):
    """
    deletes the status message with id, status_id
    """
    try:
        statustable.delete(status_id=status_id)
        return True
    # Catches any errors not finding this record
    except DoesNotExist:
        logger.error('Unable to delete user status')
        return False


def search_status(status_id):
    """
    Find and return a status message by its status_id

    Returns an empty UserStatus object if status_id does not exist
    """
    try:
        result = statustable.find_one(status_id=status_id)
        logger.info('User status found')
        return result
    # Catches any errors not finding this record
    except DoesNotExist:
        logger.error('Unable to find user status')
        return None

