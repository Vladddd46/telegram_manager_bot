from wrappers import *

'''
* Initialize user profile (only if it is already not initialized)
* when user starts bot (/start).
'''
def user_profile_init(database_file, message):
    data = json_open(database_file)
    if (message.from_user.username not in data):
        data[message.from_user.username] = {"tasks": {}}
    json_write(database_file, data)

