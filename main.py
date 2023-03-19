"""
main driver for a simple social network project
"""
# pylint: disable=W0621,C0301
import re
import sys
from csv import DictReader, DictWriter

import user_status
import users



def init_user_collection():
    """
    Creates and returns a new instance of UserCollection
    """
    return users.UserCollection()



def init_status_collection():
    """
    Creates and returns a new instance of UserStatusCollection
    """
    return user_status.UserStatusCollection()



def load_users(user_filename, user_collections):
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
        with open(user_filename, 'r', encoding="utf-8") as file:
            csv_reader = DictReader(file)
            for row in csv_reader:
                if any(v is None or v == '' for v in row.values()):
                    raise ValueError(f'Empty field in this row: {row}. ')
                user_collections.add_user(
                    row["USER_ID"],
                    row["EMAIL"],
                    row["NAME"],
                    row["LASTNAME"])
                print(f"Added account: {row}")
            return True
    except FileNotFoundError as error:
        print(f"Encountered exception while loading account list: {error}")
        return False
    except KeyError as error:
        print(
            'Wrong input file format. It should contain the following columns: ' +
            'USER_ID, EMAIL, NAME, LASTNAME. '
        )
        print(f'Detailed error message: {error}')
        return False
    except ValueError as error:
        print(f'Detailed error message: {error}')
        return False




def save_users(user_filename, user_collection):
    """
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such as an invalid filename).
    - Otherwise, it returns True.
    """
    #filename = input('Where would you like to save your user data? Enter a filename: ')
    try:
        with open(user_filename, "r+", encoding="utf-8") as file:
            writer = DictWriter(
                file,
                fieldnames=["USER_ID", "EMAIL", "NAME", "LASTNAME"],
            )
            writer.writeheader()
            for user in user_collection.database.values():
                writer.writerow(
                    {
                        "USER_ID": user.user_id,
                        "EMAIL": user.email,
                        "NAME": user.user_name,
                        "LASTNAME": user.user_last_name,
                    }
                )
        print("Successfully saved users.")
        return True
    except FileNotFoundError as error:
        print(f'Detailed error message: {error}')
        return False


def load_status_updates(status_filename, status_collections):
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
        with open(status_filename, "r", encoding="utf-8") as file:
            reader = DictReader(file)
            for row in reader:
                if any(v is None or v == '' for v in row.values()):
                    raise ValueError(f'Empty field in this row: {row}. ')
                if re.search(r'\s', row['USER_ID']):
                    raise ValueError(f'User ID cannot contain space: {row}. ')
                status_collections.add_status(
                    row["STATUS_ID"],
                    row["USER_ID"],
                    row["STATUS_TEXT"])
                print(f"Added status: {row}")
            return True
    except FileNotFoundError as error:
        print(f"File not found! Encountered exception while loading account list: {error}")
        return False
    except KeyError as error:
        print(
            'Wrong input file format. It should contain the following columns: ' +
            'STATUS_ID, USER_ID, STATUS_TEXT. '
        )
        print(f'Detailed error message: {error}')
        return False
    except ValueError as error:
        print(f'Detailed error message: {error}')
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    if not user_collection.add_user(user_id,
                                    email,
                                    user_name,
                                    user_last_name):
        print("An error occurred while trying to add new user")
        return False
    print("User was successfully added")
    return True



def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """
    if not user_collection.modify_user(user_id, email, user_name, user_last_name):
        print("User ID not found in user database.")
        return False
    print("User was successfully updated")
    return True


def delete_user(user_id, user_collection):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    #user_id = input('User ID: ')
    if not user_collection.delete_user(user_id):
        print("An error occurred while trying to delete user")
        return False
    print("User was successfully deleted")
    return True



def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    """
    #user_id = input('Enter user ID to search: ')
    result = user_collection.search_user(user_id)
    if result.user_id is None:
        print("ERROR: User does not exist")
        return None
    print(f"User ID: {result.user_id}")
    print(f"Email: {result.email}")
    print(f"Name: {result.user_name}")
    print(f"Last name: {result.user_last_name}")
    return result


def add_status(status_id, user_id, status_text, status_collection):
    """
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    if not status_collection.add_status(status_id, user_id, status_text):
        print("An error occurred while trying to add new status")
        return False
    print("New status was successfully added")
    return True


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    #status_id = input('Status ID: ')
    if not status_collection.delete_status(status_id):
        print("An error occurred while trying to delete status")
        return False
    print("Status was successfully deleted")
    return True


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    #status_id = input('Enter status ID to search: ')
    result = status_collection.search_status(status_id)
    if result.status_id is None:
        print("ERROR: Status does not exist")
        return None
    print(f"User ID: {result.user_id}")
    print(f"Status ID: {result.status_id}")
    print(f"Status text: {result.status_text}")
    return result



def save_status_updates(status_filename, status_collection):
    """
    Saves all statuses in status_collection into a CSV file

    Requirements:
    - If there is an existing file, it will overwrite it.
    - Returns False if there are any errors(such an invalid filename).
    - Otherwise, it returns True.
    """
    #filename = input('Where would you like to save your user statuses? Enter a filename: ')
    try:
        with open(status_filename, "r+", encoding="utf-8") as file:
            writer = DictWriter(
                file,
                fieldnames=["STATUS_ID", "USER_ID", "STATUS_TEXT"],
            )
            writer.writeheader()
            for status in status_collection.database.values():
                writer.writerow(
                    {
                        "STATUS_ID": status.status_id,
                        "USER_ID": status.user_id,
                        "STATUS_TEXT": status.status_text,
                    }
                )
        print("Successfully saved status updates to database.")
        return True
    except FileNotFoundError as error:
        print(f'File not found. Detailed error message: {error}')
        return False


def update_status(status_id, user_id, status_text, status_collection):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """
    if not status_collection.modify_status(status_id, user_id, status_text):
        print("An error occurred while trying to update status")
        return False
    print("Status was successfully updated")
    return True

def quit_program():
    """
    Quits program
    """
    sys.exit()

def main_menu():
    """
    creating menu
    """
    user_filename = input("Enter a file to load users:")
    status_filename = input("Enter a file to load your user status:")
    user_collection = init_user_collection()
    load_users(user_filename, user_collection)
    status_collection = init_status_collection()
    load_status_updates(status_filename, status_collection)
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': save_status_updates,
        'Q': quit_program
    }
    while True:
        user_selection = input("""
                                A: Load user database
                                B: Load status database
                                C: Add user
                                D: Update user
                                E: Search user
                                F: Delete user
                                G: Save user database to file
                                H: Add status
                                I: Update status
                                J: Search status
                                K: Delete status
                                L: Save status database to file
                                Q: Quit

                                Please enter your choice: """)
        if user_selection.upper() in menu_options:
            match user_selection:
                case 'A', 'G':
                    menu_options[user_selection](user_filename, user_collection)
                case 'C':
                    user_id = input('User ID: ')
                    email = input('User email: ')
                    user_name = input('User name: ')
                    user_last_name = input('User last name: ')
                    menu_options[user_selection](user_id, email, user_name, user_last_name, user_collection)
                case 'D':
                    user_id = input('User ID: ')
                    email = input('User email: ')
                    user_name = input('User name: ')
                    user_last_name = input('User last name: ')
                    menu_options[user_selection](user_id, email, user_name, user_last_name, user_collection)
                case 'E':
                    user_id = input("Enter a user_id to search: ")
                    menu_options[user_selection](user_id, user_collection)
                case 'F':
                    user_id = input("Enter a user_id to delete: ")
                    menu_options[user_selection](user_id, user_collection)
                case 'B', 'L':
                    menu_options[user_selection](status_filename, status_collection)
                case 'H':
                    status_id = input('Status ID: ')
                    user_id = input('User ID: ')
                    status_text = input('Status text: ')
                    menu_options[user_selection](user_id, status_id, status_text, status_collection)
                case 'I':
                    user_id = input('User ID: ')
                    status_id = input('Status ID: ')
                    status_text = input('Status text: ')
                    menu_options[user_selection](user_id, status_id, status_text, status_collection)
                case 'J':
                    status_id = input("Enter a status_id to search: ")
                    menu_options[user_selection](status_id, status_collection)
                case 'K':
                    status_id = input("Enter a status_id to delete status: ")
                    menu_options[user_selection](status_id, status_collection)
                case 'Q':
                    menu_options[user_selection]()
        else:
            print("Invalid option")


if __name__ == '__main__':
    main_menu()
