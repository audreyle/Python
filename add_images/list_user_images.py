import logging
from datetime import datetime
from pathlib import Path
from peewee import IntegrityError
from socialnetwork_model import picturetable, differences_table


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


def add_picture(picture_id, user_id, tags):
    """
    Adds a new user to the collection
    """
    try:
        tags_formatted = ''

        for i in tags:
            tags_formatted = tags_formatted + '#' + i + ' '

        picturetable.insert(picture_id=picture_id, user_id=user_id, tags=tags_formatted)
        print('Picture added')
        logger.info('New picture added')
        add_to_dir(picture_id, user_id, tags)

        return True

    except IntegrityError:
        logger.error('An error occurred')
        return False


def add_to_dir(picture_id, user_id, tags):
    try:
        # path = Path('/') / 'Users' / 'Emeka' / 'assignment_09-sirRockIII' / str(user_id)
        path = Path.cwd() / 'images' / str(user_id)

        path.mkdir(exist_ok=True)
        for i in tags:
            path = path / i
            path.mkdir(exist_ok=True)

        path = path / (picture_id + '.png')
        path.touch()
        return True

    except FileExistsError:
        print(FileExistsError)
        return True

def add_to_diff(picture_id, user_id):
    try:
        differences_table.insert(missing_picture_in_disk=picture_id, user_id=user_id)
        return True
    except IntegrityError:
        logger.error('An error occurred')
        return False


