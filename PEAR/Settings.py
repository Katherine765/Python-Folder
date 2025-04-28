def view_list(items):
    for i, item in enumerate(items):
        print(i, item)

class Settings:
    def __init__(s, users, user):
        
        functions = {'Change password': s.change_password, 'Delete account': s.delete_account, 'Quit': lambda _: 'quit'} # quit is still being passed user

        print()
        view_list(functions.keys())

        while True:
            selection = input('Selection:  ')
            
            if not (selection.isdigit() and int(selection) in range(len(functions))):
                print('Selection unsuccessful.\n')
                continue

            selection = int(selection)
            function_name = list(functions.keys())[selection]

            # separate bc of arguement
            if function_name == 'Delete account':
                result = functions[function_name](users, user)
                if result == 'account deleted':
                    return 'account deleted'
            else:
                result = functions[function_name](user)
                if result == 'quit':
                    return
    
    def change_password(s, user):
        confirmed = input('Old password:  ') == user.password
        if confirmed:
            user.password = input('New password:  ')
        else:
            print('Password change unsuccessful.')

    def delete_account(s, users, user):
        confirmed = input('Password:  ') == user.password
        if confirmed:
            username = [key for key, val in users.items() if val==user][0] # there should be exactly one
            del users[username]
            # the storage of this object is GONE but it can still function
            return 'account deleted'
        else:
            print('Account deletion unsuccessful.')