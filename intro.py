import user_mgmt

def starting_sequence():
    print('\nWELCOME TO THE CYBER PIT!')
    user_handle = user_mgmt.UserHandler()
    user = user_handle.user_prompt()
    print(f'Welcome {user}, thanks for logging in...')
