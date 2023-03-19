'''
main driver for a simple social network project.
reconciles pictures in disk vs. database and adds to differencetable.
'''
from csv import DictReader
from pathlib import Path
import users
import user_status
import list_user_images
from socialnetwork_model import ds
from log_decorator import log_function


def load_users(filename):
    """
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, 'r', encoding="UTF-8") as loaded_file:
            file = DictReader(loaded_file)
            for row in file:
                users.add_user(row['USER_ID'].strip(), row['EMAIL'].strip(), row['NAME'].strip(),
                               row['LASTNAME'].strip())
        print('File loading successful...')
        return True
    except FileNotFoundError:
        print("Could not find file")
        return False


def load_status_updates(filename):
    """
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, 'r', encoding='utf-8-sig') as loaded_file:
            file = DictReader(loaded_file)
            for row in file:
                user_status.add_status(row['STATUS_ID'], row['USER_ID'], row['STATUS_TEXT'])
        print('File loading successful...')
        return True
    except FileNotFoundError:
        print("Could not find file")
        return False


def add_user(user_id, email, user_name, user_last_name):
    """
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """

    return users.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """
    try:
        person = users.search_user(user_id)
        if person is None:
            return False
        return users.modify_user(user_id, email, user_name, user_last_name)
    except AttributeError:
        return False


def delete_user(user_id):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    try:
        person = users.search_user(user_id)
        if person is None:
            return False
        return users.delete_user(user_id)
    except AttributeError:
        return False


def search_user(user_id):
    """
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    """
    try:
        return users.search_user(user_id)
    except AttributeError:
        return False


def add_status(status_id, user_id, status_text):
    """
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """

    return user_status.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """
    try:
        status = user_status.search_status(status_id)
        if status is None:
            print('ERROR: Status does not exist')
            return False
        return user_status.modify_status(status_id, user_id, status_text)
    except AttributeError:
        return False


def delete_status(status_id):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    try:
        status = user_status.search_status(status_id)
        if status is None:
            print('ERROR: Status does not exist')
            return False
        return user_status.delete_status(status_id)
    except AttributeError:
        return False


def search_status(status_id):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """

    try:
        return user_status.search_status(status_id)
    except AttributeError:
        return False


@log_function
def add_picture(user_id, tags):
    for i in tags:
        if i.lower() not in 'abcdefjghijklmnopqrstuvwxyz#_ ':
            print('ERROR: Only letters, # and _ characters are allowed'
                  ' for the tags')
            return False
    space_delete = tags.replace(" ", "")
    x = space_delete.split('#')
    if '' in x:
        x.remove('')
    try:
        person = users.search_user(user_id)
        if person is None:
            print("ERROR: User does not exist.")
            return False
        num = 1
        while True:
            num_format = str(num).zfill(10)
            if find_picture(num_format) is False:
                picture_id = num_format
                break
            num += 1
        list_user_images.add_picture(picture_id, user_id, x)
        return True
    except AttributeError:
        return False


def find_picture(picture_id):
    q = ds['picturetable'].find_one(picture_id=picture_id)
    if isinstance(q, dict):
        return True
    return False

@log_function
def list_images(user_id, reconcile=False):
    disk_pics = []
    try:
        def list_user_image(_path):
            if _path.is_file():
                # Print out only python files
                if _path.suffix == '.png':

                    path_form = str(_path.absolute()).split('\\')
                    if not reconcile:
                        print((user_id, _path.absolute(), path_form[-1]))
                    if reconcile:
                        # disk_pics.append(path_form[-1].strip('.png'))
                        disk_pics.append(_path.name.strip('.png'))
            elif 'venv' in str(_path.absolute()):
                # Skip the venv folders
                pass
            else:
                # Since it's a directory, let's recurse into them
                for i in _path.iterdir():
                    list_user_image(i)

        # Let's list files in our project folder
        # path = Path('/') / 'Users' / 'Emeka' / 'assignment_09-sirRockIII' / str(user_id)
        path = Path.cwd() / 'images' / str(user_id)
        list_user_image(path)
        if reconcile:
            return {user_id: disk_pics}
        return True
    except FileNotFoundError:
        print('ERROR: File not found')
        return False


def reconcile_images():
    all_users_db = []
    u = list(ds['usertable'].all())
    picture = []
    all_user_pics_db = {}
    all_user_pics_disk = {}
    for i in u:
        all_users_db.append(i['user_id'])
    for user in all_users_db:
        p = list(ds['picturetable'].find(user_id=user))
        for pic in p:
            picture.append(pic['picture_id'])
        all_user_pics_db[user] = picture
        try:
            print(f'list images of {user}')
            all_user_pics_disk.update(list_images(user, reconcile=True))
        except:
            print(f'FAIL DURING list images of {user}')
            pass
    pic_discrepancy = []
    for user in all_users_db:
        for i in all_user_pics_disk.get(user):
            if i not in all_user_pics_db.get(user):
                pic_discrepancy.append(i)
        for i in all_user_pics_db.get(user):
            if i not in all_user_pics_disk.get(user):
                pic_discrepancy.append(i)
    print(f'ATTENTION: {len(pic_discrepancy)} discrepancy when comparing disk to database records')
    if len(pic_discrepancy) > 0:
        for i in pic_discrepancy:
            print(i)
    for picture_id in pic_discrepancy:
        get_user_id = ds['picturetable'].find_one(picture_id=picture_id)
        print(get_user_id['user_id'])
        list_user_images.add_to_diff(picture_id, get_user_id['user_id'])
    return True
