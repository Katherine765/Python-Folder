# in vs code, only works if New PEAR is the only folder open
# the problem is that any time an app is updated, the user objects still holds a copy of an object from an app that hasn't been updated. might not have same functions or data structures

# maybe get rid of main functions and just run init
# ugh but then i have to worry abt parameters again

# some of the daily details are messed up

import pickle
from User import User
import os
from To_do import To_do
from Weather import Weather
from Logout import Logout
from Settings import Settings
from collections import defaultdict

# the users dictionary holds w/ username indexes and user object values
# a user object contains a dictionary w/ app name indexes and app storage values
if os.path.getsize('Users.txt') == 0:
    users = {}
else:
    with open('Users.txt', 'rb') as f:
        users = pickle.load(f)

def view_list(items):
    for i, item in enumerate(items):
        print(i, item)

def update_file():
    with open('Users.txt', 'wb') as f:
        pickle.dump(users, f)    


def main():
    logged_in = False
    while not logged_in:
        username = input('Username:  ')
        if username in users.keys():
            user = users[username]
            password = input('Password:  ')
            if password == user.password:
                logged_in = True
            else:
                ('Login unsuccessful.\n')
        else:
            password = input('New password:  ')
            users[username] = User(password)
            update_file()
            user = users[username]
            logged_in = True
    
    ###########  ADD APPS HERE ###########  ADD APPS HERE ###########  ADD APPS HERE ###########  ADD APPS HERE ###########  ADD APPS HERE #
    all_apps ={'To do': To_do, 'Weather':Weather, 'Settings': Settings, 'Logout': Logout}
    arguments = defaultdict(tuple, {'Settings': (users, user)})

    while True:
        print()
        view_list(all_apps.keys()) # print menu
        selection = input('Selection:  ')

        if not (selection.isdigit() and int(selection) in range(len(all_apps))):
            print('Selection unsuccessful.\n')
            continue

        selection = int(selection)
        app_name = list(all_apps.keys())[selection]

        if app_name in user.app_storages.keys():
            app_obj = all_apps[app_name](*arguments[app_name],user.app_storages[app_name]) # pass the storage
            print('storage passed')
        else: 
            app_obj = all_apps[app_name](*arguments[app_name])

        #app_obj.main(*arguments[app_name])
        if hasattr(app_obj,'storage'):
            print('storing')
            user.app_storages[app_name] = app_obj.storage
            update_file()

        # if settings deleted the account
        if not user in users.values():
            quit()

main()