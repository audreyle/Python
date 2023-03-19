#pylint: disable=R0903
"""
Load status_updates.csv to StatusUpdates table.
Make sure to call load_users from menu.py first.
"""
import multiprocessing
from multiprocessing import Process, Queue
import time

import pandas

import pymongo
from pymongo.errors import DuplicateKeyError

import mongodb_connection

user_accounts_collection = mongodb_connection.database['UserAccounts']

class ProcessX:
    """
    Create a Process class which takes a name, queue and mongodb connection
    """
    def __init__(self, name):
        self.name = name
        self.queue = Queue
        self.mongo_client = None
        self.mongo_db = None


    def add_status_updates(self, queue):
        """
        Get result from queue and insert to db. Be sure to change self.mongodb to
        self.mongo_client["test_social_network_data"] for testing!
        """
        print(f"{self.name}: Started", flush=True)
        # Open a separate mongodb connection for each process
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["social_network_data"]
        # use for unittest
        #self.mongo_db = self.mongo_client["test_social_network_data"]

        while True:
            # Get the chunk of status_updates to put in the database
            status_updates_list = queue.get()
            # check for stop
            if status_updates_list is None:
                break
            for chunk_dict in status_updates_list:
                try:
                    self.mongo_db.StatusUpdates.insert_one(chunk_dict)
                except DuplicateKeyError:
                    print(f"{self.name}:Duplicate Key Error")

        # all done
        print(f"{self.name}: Done", flush=True)
        self.mongo_client.close()


def main():
    """
    Set up processes and queues
    """
    queue_01 = Queue()
    queue_02 = Queue()
    # q3 = Queue()
    # q4 = Queue()
    # q5 = Queue()
    p_1 = ProcessX('process_01')
    p_2 = ProcessX('process_02')
    # p3 = ProcessX('process_03')
    # p4 = ProcessX('process_04')
    # p5 = ProcessX('process_05')
    # Start processes to store StatusUpdate records into the social_network database
    process_01 = Process(target=p_1.add_status_updates, args=(queue_01,))
    process_02 = Process(target=p_2.add_status_updates, args=(queue_02,))
    # process_03 = Process(target=p3.add_status_updates, args=(q3,))
    # process_04 = Process(target=p4.add_status_updates, args=(q4,))
    # process_05 = Process(target=p5.add_status_updates, args=(q5,))
    process_01.start()
    process_02.start()
    # process_03.start()
    # process_04.start()
    # process_05.start()

    # Make sure the processes have actually started
    while True:
        if process_01.is_alive():
            break
    while True:
        if process_02.is_alive():
            break
    # while True:
    #     if process_03.is_alive():
    #         break
    # while True:
    #     if process_04.is_alive():
    #         break

    csv_reader = pandas.read_csv('status_updates.csv', chunksize=10000, iterator=True)
    send_to_queue = 1
    chunk_number = 1
    for chunk in csv_reader:
        # create a list to append status updates to avoid dropping an entire chunk if one user_id
        # does not exist in UserAccounts
        new_status_data_chunk = []
        for row in chunk.iterrows():
            # check if user_id exists in UserAccounts
            result = user_accounts_collection.count_documents({'_id': row['USER_ID']})
            if result == 1: # if user_id exists the result is 1
                # append status update to list as a dictionary with these keys
                new_status_data_chunk.append({
                        "_id": row['STATUS_ID'],
                        "USER_ID": row['USER_ID'],
                        "STATUS_TEXT": row['STATUS_TEXT']
                    })
            else:
                print(f"There is no user with id '{row['USER_ID']}' in the database. "
                      f"Can not add a status update for a non_existing user.")
                continue
        # rename list of acceptable status updates
        chunk_dict = new_status_data_chunk
        # Distribute chunks in round robbin fashion to processes 1 - 5
        if send_to_queue == 1:
            # Send this chunk to Process 01
            queue_01.put(chunk_dict)
            print(f"Sent chunk {chunk_number} to process01", flush=True)
            send_to_queue = 2
        elif send_to_queue == 2:
            # Send this chunk to Process 02
            queue_02.put(chunk_dict)
            print(f"Sent chunk {chunk_number} to process02", flush=True)
            send_to_queue = 1
        # elif send_to_queue == 3:
        #     # Send this chunk to Process 03
        #     q3.put(chunk_dict)
        #     # print(f"Sent chunk {chunk_number} to process03", flush=True)
        #     send_to_queue = 4
        # elif send_to_queue == 4:
        #     # Send this chunk to Process 04
        #     q4.put(chunk_dict)
        #     # print(f"Sent chunk {chunk_number} to process04", flush=True)
        #     send_to_queue = 5
        # elif send_to_queue == 5:
        #     # Send this chunk to Process 04
        #     q4.put(chunk_dict)
        #     # print(f"Sent chunk {chunk_number} to process04", flush=True)
        #     send_to_queue = 1
        chunk_number += 1

    queue_01.put(None)  # Stop process_01
    queue_02.put(None)  # Stop process_02
    # q3.put(None)  # Stop process_03
    # q4.put(None)  # Stop process_04
    # q5.put(None)  # Stop process_05

    process_01.join()
    process_02.join()
    # process_03.join()
    # process_04.join()
    # process_05.join()


if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = round(time.time() - start_time, 2)
    print(f"{elapsed_time}s passed")
    print(multiprocessing.cpu_count())
